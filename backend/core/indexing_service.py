import asyncio
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import Session
from src.core.database import File, Slide, CostTracking
from src.core.scanner import FileScanner
from src.parsers import ParserFactory
from src.core.llm_service import LLMService
from src.search.vector_store import VectorStore

class IndexingService:
    def __init__(self, db_session: Session, vector_store: VectorStore, llm_service: LLMService):
        self.db_session = db_session
        self.vector_store = vector_store
        self.llm_service = llm_service
        self.scanner = FileScanner()
        self.parser_factory = ParserFactory()

    async def index_file(self, file_path: Path, file_type: str, file_size: int) -> bool:
        """Index a single file."""
        try:
            # Check if file already indexed with same hash
            file_hash = self.scanner.compute_file_hash(file_path)
            existing = self.db_session.query(File).filter(
                File.path == str(file_path),
                File.hash == file_hash
            ).first()

            if existing:
                print(f"Skipping {file_path} (already indexed)")
                return True

            # Get file metadata
            metadata = self.scanner.get_file_metadata(file_path)

            # Parse file
            parsed = self.parser_factory.parse_file(file_path, file_type)
            if not parsed.get('success'):
                print(f"Failed to parse {file_path}: {parsed.get('error')}")
                return False

            # Prepare content for LLM
            content = parsed.get('content', '')

            # Handle images separately
            if parsed.get('needs_vision'):
                analysis = await self.llm_service.analyze_image(file_path)
            else:
                analysis = await self.llm_service.summarize_text(content, file_type)

            if not analysis.get('success'):
                print(f"Failed to analyze {file_path}: {analysis.get('error')}")
                return False

            # Get embedding
            embedding_text = f"{analysis.get('summary', '')} {analysis.get('keywords', '')}"
            embedding = await self.llm_service.get_embedding(embedding_text)

            # Create or update file record
            file_record = self.db_session.query(File).filter(File.path == str(file_path)).first()
            if not file_record:
                file_record = File(
                    path=str(file_path),
                    hash=file_hash,
                    type=file_type,
                    size=file_size,
                    ctime=metadata['ctime'],
                    mtime=metadata['mtime']
                )
                self.db_session.add(file_record)
                self.db_session.flush()

            # Update analysis results
            file_record.summary = analysis.get('summary', '')
            file_record.keywords = analysis.get('keywords', '')
            file_record.category = analysis.get('category', 'unknown')
            file_record.confidence = analysis.get('confidence', 0.0)
            file_record.source_model = analysis.get('model', '')
            file_record.cost_tokens = analysis.get('tokens', 0)
            file_record.status = 'completed'
            file_record.indexed_at = datetime.utcnow()

            self.db_session.commit()

            # Store embedding
            if embedding:
                self.vector_store.add_file_embedding(file_record.file_id, embedding)

            # Track cost
            self._track_cost(file_record.file_id, 'summarize', analysis.get('model', ''), analysis.get('tokens', 0))

            # Handle slides for presentations
            if file_type == 'pptx' and 'slides' in parsed:
                await self._index_slides(file_record.file_id, parsed['slides'])

            print(f"✓ Indexed: {file_path}")
            return True

        except Exception as e:
            print(f"Error indexing {file_path}: {e}")
            return False

    async def _index_slides(self, file_id: int, slides_data: list):
        """Index individual slides from a presentation."""
        for slide_data in slides_data:
            try:
                # Analyze slide
                slide_text = f"{slide_data.get('text', '')} {slide_data.get('notes', '')}"
                if not slide_text.strip():
                    continue

                analysis = await self.llm_service.summarize_text(slide_text, 'slide')
                if not analysis.get('success'):
                    continue

                # Get embedding
                embedding_text = f"{analysis.get('summary', '')} {analysis.get('keywords', '')}"
                embedding = await self.llm_service.get_embedding(embedding_text)

                # Create slide record
                slide_record = Slide(
                    file_id=file_id,
                    page_number=slide_data['page_number'],
                    title=slide_data.get('text', '')[:200],
                    summary=analysis.get('summary', ''),
                    keywords=analysis.get('keywords', ''),
                    notes=slide_data.get('notes', ''),
                    confidence=analysis.get('confidence', 0.0),
                    source_model=analysis.get('model', ''),
                    cost_tokens=analysis.get('tokens', 0),
                    indexed_at=datetime.utcnow()
                )

                self.db_session.add(slide_record)
                self.db_session.flush()

                # Store embedding
                if embedding:
                    self.vector_store.add_slide_embedding(slide_record.slide_id, embedding)

                self._track_cost(file_id, 'summarize_slide', analysis.get('model', ''), analysis.get('tokens', 0))

            except Exception as e:
                print(f"Error indexing slide {slide_data.get('page_number')}: {e}")

        self.db_session.commit()

    def _track_cost(self, file_id: int, operation: str, model: str, tokens: int):
        """Track API costs."""
        # Cost estimation (adjust based on actual pricing)
        cost_per_1k_tokens = {
            # Claude models
            'claude-3-5-sonnet-20241022': 0.003,
            'claude-3-5-haiku-20241022': 0.001,
            # OpenAI models
            'gpt-4o-mini': 0.00015,
            'text-embedding-3-small': 0.0001,
            # Kimi models (Moonshot AI pricing)
            'moonshot-v1-8k': 0.012 / 1000,  # ¥12/1M tokens ≈ $0.012/1K
            'moonshot-v1-32k': 0.024 / 1000,  # ¥24/1M tokens ≈ $0.024/1K
            'moonshot-v1-128k': 0.060 / 1000,  # ¥60/1M tokens ≈ $0.060/1K
        }

        cost = (tokens / 1000) * cost_per_1k_tokens.get(model, 0.001)

        cost_record = CostTracking(
            date=datetime.utcnow(),
            operation=operation,
            model=model,
            tokens=tokens,
            cost_usd=cost,
            file_id=file_id
        )

        self.db_session.add(cost_record)
        self.db_session.commit()

    async def index_all(self):
        """Index all files in configured directories."""
        print("Starting full indexing...")
        total = 0
        success = 0

        for file_path, file_type, file_size in self.scanner.scan_directories():
            total += 1
            if await self.index_file(file_path, file_type, file_size):
                success += 1

            # Simple rate limiting
            await asyncio.sleep(0.1)

        print(f"\nIndexing complete: {success}/{total} files indexed successfully")
