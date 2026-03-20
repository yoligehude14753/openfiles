import click
import asyncio
import uvicorn
from pathlib import Path
from rich.console import Console
from rich.table import Table
from src.core.config import settings
from src.core.database import init_db, get_session
from src.core.llm_service import LLMService
from src.search.vector_store import VectorStore
from src.core.indexing_service import IndexingService
from src.search.search_service import SearchService

console = Console()


@click.group()
def cli():
    """ChatFiles - Chat with your files. Locally. Privately."""
    pass


@cli.command()
def init():
    """Initialize the database."""
    try:
        db_path = Path(settings.database_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        init_db(str(db_path))
        console.print(f"[green]Database initialized at: {db_path}[/green]")
    except Exception as e:
        console.print(f"[red]Error initializing database: {e}[/red]")


@cli.command()
def index():
    """Index all files in configured directories."""
    try:
        db_path = Path(settings.database_path)
        if not db_path.exists():
            console.print("[yellow]Database not found. Initializing...[/yellow]")
            db_path.parent.mkdir(parents=True, exist_ok=True)
            init_db(str(db_path))

        engine = init_db(str(db_path))
        session = get_session(engine)
        vector_store = VectorStore(str(db_path))
        llm_service = LLMService()
        indexing_service = IndexingService(session, vector_store, llm_service)

        console.print(f"[blue]Scanning: {', '.join(str(d) for d in settings.scan_dirs_list)}[/blue]")
        console.print(f"[blue]LLM Provider: {settings.llm_provider}[/blue]")

        asyncio.run(indexing_service.index_all())
        vector_store.close()
        console.print("[green]Indexing complete![/green]")

    except Exception as e:
        console.print(f"[red]Error during indexing: {e}[/red]")
        import traceback
        traceback.print_exc()


@cli.command()
@click.confirmation_option(prompt="This will delete all indexed data and rebuild from scratch. Continue?")
def reindex():
    """Clear all indexed data and rebuild from scratch."""
    try:
        db_path = Path(settings.database_path)
        if not db_path.exists():
            console.print("[yellow]No database found. Running fresh init + index.[/yellow]")
        else:
            engine = init_db(str(db_path))
            session = get_session(engine)
            from src.core.database import File, Slide, CostTracking, Context, Task, Conversation, Message
            for table in [Message, Conversation, Slide, Context, Task, CostTracking, File]:
                deleted = session.query(table).delete()
                console.print(f"  Cleared {table.__tablename__}: {deleted} rows")
            session.commit()

            vector_store = VectorStore(str(db_path))
            vector_store.conn.execute("DELETE FROM file_embeddings")
            vector_store.conn.execute("DELETE FROM slide_embeddings")
            vector_store.conn.commit()
            vector_store.close()
            console.print("[green]All old data cleared.[/green]")

        console.print("[blue]Starting fresh index...[/blue]")
        db_path.parent.mkdir(parents=True, exist_ok=True)
        engine = init_db(str(db_path))
        session = get_session(engine)
        vector_store = VectorStore(str(db_path))
        llm_service = LLMService()
        indexing_service = IndexingService(session, vector_store, llm_service)

        console.print(f"[blue]Provider: {settings.llm_provider} | Embedding: {settings.embedding_provider}[/blue]")
        asyncio.run(indexing_service.index_all())
        vector_store.close()
        console.print("[green]Reindex complete![/green]")

    except Exception as e:
        console.print(f"[red]Error during reindex: {e}[/red]")
        import traceback
        traceback.print_exc()


@cli.command()
@click.argument("query")
@click.option("--limit", default=10, help="Number of results")
@click.option("--type", "search_type", default="files", type=click.Choice(["files", "slides"]))
def search(query: str, limit: int, search_type: str):
    """Search indexed files."""
    try:
        db_path = Path(settings.database_path)
        if not db_path.exists():
            console.print("[red]Database not initialized. Run 'chatfiles init' first.[/red]")
            return

        engine = init_db(str(db_path))
        session = get_session(engine)
        vector_store = VectorStore(str(db_path))
        llm_service = LLMService()
        search_service = SearchService(session, vector_store, llm_service)

        console.print(f"[blue]Searching: {query}[/blue]")

        if search_type == "files":
            results = asyncio.run(search_service.search_files(query, limit=limit))
        else:
            results = asyncio.run(search_service.search_slides(query, limit=limit))

        if not results:
            console.print("[yellow]No results found.[/yellow]")
            return

        if search_type == "files":
            table = Table(title=f"Results ({len(results)} files)")
            table.add_column("Path", style="cyan", max_width=50)
            table.add_column("Type", style="magenta")
            table.add_column("Summary", style="white", max_width=60)
            table.add_column("Score", style="green")

            for r in results:
                table.add_row(
                    r["path"],
                    r["type"],
                    (r.get("summary", "") or "")[:80],
                    f"{r['similarity']:.3f}",
                )
        else:
            table = Table(title=f"Results ({len(results)} slides)")
            table.add_column("File", style="cyan")
            table.add_column("Page", style="magenta")
            table.add_column("Summary", style="white", max_width=60)
            table.add_column("Score", style="green")

            for r in results:
                table.add_row(
                    Path(r["file_path"]).name,
                    str(r["page_number"]),
                    (r.get("summary", "") or "")[:80],
                    f"{r['similarity']:.3f}",
                )

        console.print(table)
        vector_store.close()

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        import traceback
        traceback.print_exc()


@cli.command()
def stats():
    """Show indexing statistics."""
    try:
        db_path = Path(settings.database_path)
        if not db_path.exists():
            console.print("[red]Database not initialized.[/red]")
            return

        engine = init_db(str(db_path))
        session = get_session(engine)

        from src.core.database import File, Slide, CostTracking
        from sqlalchemy import func

        total_files = session.query(func.count(File.file_id)).scalar()
        completed = session.query(func.count(File.file_id)).filter(File.status == "completed").scalar()
        total_slides = session.query(func.count(Slide.slide_id)).scalar()
        total_cost = session.query(func.sum(CostTracking.cost_usd)).scalar() or 0.0
        total_tokens = session.query(func.sum(CostTracking.tokens)).scalar() or 0

        table = Table(title="ChatFiles Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Total Files", str(total_files))
        table.add_row("Indexed Files", str(completed))
        table.add_row("Total Slides", str(total_slides))
        table.add_row("Total Tokens", f"{total_tokens:,}")
        table.add_row("Total Cost", f"${total_cost:.4f}")
        table.add_row("LLM Provider", settings.llm_provider)
        table.add_row("Embedding Provider", settings.embedding_provider)

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@cli.command()
@click.option("--host", default=None, help="Host to bind to")
@click.option("--port", default=None, type=int, help="Port to bind to")
def serve(host: str, port: int):
    """Start the ChatFiles web server."""
    host = host or settings.web_host
    port = port or settings.web_port

    db_path = Path(settings.database_path)
    if not db_path.exists():
        console.print("[yellow]Database not found. Initializing...[/yellow]")
        db_path.parent.mkdir(parents=True, exist_ok=True)
        init_db(str(db_path))

    console.print(f"[green]Starting ChatFiles at http://{host}:{port}[/green]")
    console.print("[dim]Press Ctrl+C to stop[/dim]")

    uvicorn.run(
        "src.api.app:app",
        host=host,
        port=port,
        reload=False,
    )


if __name__ == "__main__":
    cli()
