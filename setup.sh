#!/bin/bash
set -e

echo "╔════════════════════════════════════════╗"
echo "║         OpenFiles Setup                ║"
echo "║  AI assistant for your local files.    ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required. Install from https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "✓ Python $PYTHON_VERSION found"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
echo "✓ Virtual environment activated"

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "✓ Dependencies installed"

# Setup environment
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ Created .env from template"
else
    echo "✓ .env already exists"
fi

# Create data directories
mkdir -p data/db data/cache data/thumbnails
echo "✓ Data directories created"

# Initialize database
python3 main.py init
echo "✓ Database initialized"

# Check Ollama
echo ""
if command -v ollama &> /dev/null; then
    echo "✓ Ollama detected"
    echo "  Pulling recommended models..."
    ollama pull qwen3-vl:8b 2>/dev/null || echo "  (Pull manually: ollama pull qwen3-vl:8b)"
    ollama pull EntropyYue/jina-embeddings-v2-base-zh 2>/dev/null || echo "  (Pull manually: ollama pull EntropyYue/jina-embeddings-v2-base-zh)"
else
    echo "⚠ Ollama not found. Install from https://ollama.com for local LLM support."
    echo "  Or set OPENAI_API_KEY in .env to use OpenAI instead."
fi

# Frontend setup
echo ""
if command -v node &> /dev/null; then
    echo "Setting up frontend..."
    cd frontend && npm install -q && cd ..
    echo "✓ Frontend dependencies installed"
else
    echo "⚠ Node.js not found. Install from https://nodejs.org for the web UI."
fi

echo ""
echo "════════════════════════════════════════"
echo "  Setup complete!"
echo ""
echo "  Start the server:"
echo "    source venv/bin/activate"
echo "    python main.py serve"
echo ""
echo "  Start frontend (separate terminal):"
echo "    cd frontend && npm run dev"
echo ""
echo "  Or use Docker:"
echo "    docker compose up"
echo "════════════════════════════════════════"
