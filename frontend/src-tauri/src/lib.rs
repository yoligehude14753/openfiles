use tauri::{
    menu::{Menu, MenuItem},
    tray::TrayIconBuilder,
    Manager, WindowEvent,
};
use tauri_plugin_shell::ShellExt;
use std::sync::Mutex;

struct ServerChild(Mutex<Option<tauri_plugin_shell::process::CommandChild>>);

const WINDOW_WIDTH: f64 = 680.0;
const INITIAL_HEIGHT: f64 = 44.0;

fn toggle_spotlight(app: &tauri::AppHandle) {
    if let Some(window) = app.get_webview_window("spotlight") {
        if window.is_visible().unwrap_or(false) {
            let _ = window.hide();
            let _ = window.set_size(tauri::LogicalSize::new(WINDOW_WIDTH, INITIAL_HEIGHT));
        } else {
            let _ = window.set_size(tauri::LogicalSize::new(WINDOW_WIDTH, INITIAL_HEIGHT));
            if let Some(monitor) = app.primary_monitor().ok().flatten() {
                let screen = monitor.size();
                let scale = monitor.scale_factor();
                let sw = screen.width as f64 / scale;
                let sh = screen.height as f64 / scale;
                let x = (sw - WINDOW_WIDTH) / 2.0;
                let y = sh * 0.22;
                let _ = window.set_position(tauri::LogicalPosition::new(x, y));
            }
            let _ = window.show();
            let _ = window.set_focus();
        }
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(
            tauri_plugin_global_shortcut::Builder::new()
                .with_handler(|app, _shortcut, event| {
                    if event.state == tauri_plugin_global_shortcut::ShortcutState::Pressed {
                        toggle_spotlight(app);
                    }
                })
                .build(),
        )
        .manage(ServerChild(Mutex::new(None)))
        .setup(|app| {
            // Register global shortcut
            use tauri_plugin_global_shortcut::GlobalShortcutExt;
            app.global_shortcut()
                .register("CmdOrCtrl+Shift+Space")
                .expect("failed to register global shortcut");

            // Spawn Python sidecar (skip in dev mode if binary not bundled)
            match app.shell().sidecar("openfiles-server") {
                Ok(sidecar) => match sidecar.spawn() {
                    Ok((_rx, child)) => {
                        println!("OpenFiles server started (sidecar)");
                        let state = app.state::<ServerChild>();
                        *state.0.lock().unwrap() = Some(child);
                    }
                    Err(e) => {
                        eprintln!("Sidecar not started: {}. Assuming external server.", e);
                    }
                },
                Err(_) => {
                    println!("No sidecar binary found — using external backend at localhost:8000");
                }
            }

            // Build tray menu
            let show_i = MenuItem::with_id(app, "show", "Search (⌘⇧Space)", true, None::<&str>)?;
            let quit_i = MenuItem::with_id(app, "quit", "Quit OpenFiles", true, None::<&str>)?;
            let menu = Menu::with_items(app, &[&show_i, &quit_i])?;

            TrayIconBuilder::new()
                .icon(app.default_window_icon().unwrap().clone())
                .icon_as_template(true)
                .menu(&menu)
                .on_menu_event(|app, event| match event.id.as_ref() {
                    "show" => toggle_spotlight(app),
                    "quit" => {
                        let state = app.state::<ServerChild>();
                        if let Some(child) = state.0.lock().unwrap().take() {
                            let _ = child.kill();
                        }
                        std::process::exit(0);
                    }
                    _ => {}
                })
                .on_tray_icon_event(|tray, event| {
                    if let tauri::tray::TrayIconEvent::Click { .. } = event {
                        toggle_spotlight(tray.app_handle());
                    }
                })
                .build(app)?;

            // Auto-hide on focus loss
            if let Some(window) = app.get_webview_window("spotlight") {
                let w = window.clone();
                window.on_window_event(move |event| {
                    if let WindowEvent::Focused(false) = event {
                        let _ = w.hide();
                    }
                });
            }

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
