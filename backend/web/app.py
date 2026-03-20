from flask import Flask, render_template, request, jsonify
from pathlib import Path
import asyncio
from src.core.config import settings
from src.core.database import init_db, get_session
from src.core.llm_service import LLMService
from src.search.vector_store import VectorStore
from src.search.search_service import SearchService

app = Flask(__name__)

def get_search_service():
    db_path = Path(settings.database_path)
    engine = init_db(str(db_path))
    session = get_session(engine)
    vector_store = VectorStore(str(db_path))
    llm_service = LLMService()
    return SearchService(session, vector_store, llm_service), vector_store

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query', '')
    search_type = data.get('type', 'files')
    limit = data.get('limit', 10)

    if not query:
        return jsonify({'error': 'Query is required'}), 400

    try:
        search_service, vector_store = get_search_service()

        if search_type == 'files':
            results = asyncio.run(search_service.search_files(query, limit=limit))
        else:
            results = asyncio.run(search_service.search_slides(query, limit=limit))

        vector_store.close()
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def stats():
    try:
        db_path = Path(settings.database_path)
        engine = init_db(str(db_path))
        session = get_session(engine)

        from src.core.database import File, Slide, CostTracking
        from sqlalchemy import func

        total_files = session.query(func.count(File.file_id)).scalar()
        completed_files = session.query(func.count(File.file_id)).filter(File.status == 'completed').scalar()
        total_slides = session.query(func.count(Slide.slide_id)).scalar()
        total_cost = session.query(func.sum(CostTracking.cost_usd)).scalar() or 0.0
        total_tokens = session.query(func.sum(CostTracking.tokens)).scalar() or 0

        return jsonify({
            'total_files': total_files,
            'indexed_files': completed_files,
            'total_slides': total_slides,
            'total_tokens': total_tokens,
            'total_cost': total_cost
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def run_server(host='127.0.0.1', port=5166):
    app.run(host=host, port=port, debug=True)
