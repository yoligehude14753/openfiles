# Contributing to ChatFiles

Thank you for your interest in contributing! Here's how to get started.

## Development Setup

```bash
# Clone the repo
git clone https://github.com/yourname/chatfiles.git
cd chatfiles

# Run the setup script
./setup.sh

# Start backend (with auto-reload)
source venv/bin/activate
python main.py serve

# Start frontend (in another terminal)
cd frontend
npm run dev
```

## Project Structure

```
chatfiles/
├── src/                    # Python backend
│   ├── api/                # FastAPI routes
│   ├── chat/               # RAG chat engine
│   ├── core/               # Config, DB, LLM, scanner, indexing
│   ├── parsers/            # File type parsers
│   ├── search/             # Vector store & search service
│   └── watcher/            # File system watcher
├── frontend/               # React frontend
│   └── src/
│       ├── components/     # UI components
│       ├── services/       # API client
│       ├── stores/         # Zustand state
│       └── i18n/           # Translations
├── main.py                 # CLI entry point
├── requirements.txt        # Python dependencies
└── docker-compose.yml      # Docker setup
```

## How to Contribute

### Adding a New Parser

1. Create `src/parsers/your_parser.py` extending `BaseParser`
2. Implement `can_parse()` and `parse()` methods
3. Register it in `src/parsers/__init__.py`
4. Add file type to `src/core/scanner.py` if needed

### Adding a New LLM Provider

1. Add the provider config to `src/core/config.py`
2. Implement the provider methods in `src/core/llm_service.py`
3. Update `.env.example` with the new settings

### Frontend Changes

1. Components are in `frontend/src/components/`
2. Use Tailwind CSS for styling
3. Add translations to both `en.json` and `zh.json`

## Guidelines

- Write clear, self-documenting code
- Add type hints to Python functions
- Use TypeScript strict mode for frontend code
- Test your changes locally before submitting
- Keep PRs focused — one feature or fix per PR
- Update documentation if your change affects user-facing behavior

## Reporting Issues

Please include:
- OS and version
- Python/Node version
- Steps to reproduce
- Expected vs actual behavior
- Error logs if applicable

## Code of Conduct

Be respectful. Be constructive. We're all here to build something useful.
