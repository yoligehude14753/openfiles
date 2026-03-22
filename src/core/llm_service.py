import json
import base64
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

import httpx
import tiktoken

from src.core.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self):
        self.provider = settings.llm_provider
        self.embedding_provider = settings.embedding_provider
        self.encoding = tiktoken.get_encoding("cl100k_base")

        self._compatible_client = None
        self._anthropic_client = None
        self._openai_client = None
        self._kimi_client = None
        self._local_embedding_model = None

        self._init_providers()

    def _init_providers(self):
        api_key = settings.effective_compatible_api_key
        base_url = settings.effective_compatible_base_url
        if api_key and base_url:
            try:
                import openai
                self._compatible_client = openai.OpenAI(
                    api_key=api_key,
                    base_url=base_url,
                )
                logger.info("OpenAI-compatible client initialized (base: %s)", base_url)
            except Exception as e:
                logger.warning("Failed to init OpenAI-compatible client: %s", e)

        if settings.anthropic_api_key:
            try:
                import anthropic
                self._anthropic_client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
            except Exception as e:
                logger.warning("Failed to init Anthropic client: %s", e)

        if settings.openai_api_key:
            try:
                import openai
                self._openai_client = openai.OpenAI(api_key=settings.openai_api_key)
            except Exception as e:
                logger.warning("Failed to init OpenAI client: %s", e)

        if settings.kimi_api_key:
            try:
                import openai
                self._kimi_client = openai.OpenAI(
                    api_key=settings.kimi_api_key,
                    base_url="https://api.moonshot.cn/v1",
                )
            except Exception as e:
                logger.warning("Failed to init Kimi client: %s", e)

        if self.embedding_provider == "local":
            self._init_local_embedding()

    def _init_local_embedding(self):
        try:
            from sentence_transformers import SentenceTransformer
            logger.info("Loading local embedding model: %s", settings.embedding_model)
            self._local_embedding_model = SentenceTransformer(settings.embedding_model)
        except ImportError:
            logger.warning("sentence-transformers not installed.")
        except Exception as e:
            logger.warning("Failed to load local embedding model: %s", e)

    def count_tokens(self, text: str) -> int:
        return len(self.encoding.encode(text))

    def chunk_text(self, text: str, chunk_size: int = None) -> List[str]:
        if chunk_size is None:
            chunk_size = settings.chunk_size
        tokens = self.encoding.encode(text)
        chunks = []
        for i in range(0, len(tokens), chunk_size):
            chunks.append(self.encoding.decode(tokens[i:i + chunk_size]))
        return chunks

    # ── Chat Completion ──────────────────────────────────────────

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False,
        temperature: float = 0.7,
    ):
        if self.provider in ("yunwu", "openai-compatible") and self._compatible_client:
            return await self._chat_compatible(messages, stream, temperature)
        elif self.provider == "ollama":
            return await self._chat_ollama(messages, stream, temperature)
        elif self.provider == "openai" and self._openai_client:
            return await self._chat_openai(messages, stream, temperature)
        elif self.provider == "claude" and self._anthropic_client:
            return await self._chat_claude(messages, stream, temperature)
        elif self.provider == "kimi" and self._kimi_client:
            return await self._chat_kimi(messages, stream, temperature)
        else:
            raise ValueError(
                f"No available provider for '{self.provider}'. "
                "Check your API keys in .env"
            )

    async def _chat_compatible(self, messages, stream, temperature):
        model = settings.effective_compatible_model
        instructions = None
        input_msgs = []
        for m in messages:
            if m["role"] == "system":
                instructions = m["content"]
            else:
                input_msgs.append(m)

        kwargs = {
            "model": model,
            "input": input_msgs,
            "temperature": temperature,
            "stream": stream,
        }
        if instructions:
            kwargs["instructions"] = instructions

        if stream:
            return self._stream_compatible_responses(kwargs)

        response = self._compatible_client.responses.create(**kwargs)
        return response.output_text

    async def _stream_compatible_responses(self, kwargs):
        stream = self._compatible_client.responses.create(**kwargs)
        for event in stream:
            if hasattr(event, "type") and event.type == "response.output_text.delta":
                if hasattr(event, "delta"):
                    yield event.delta

    async def _chat_ollama(self, messages, stream, temperature):
        url = f"{settings.ollama_host}/api/chat"
        payload = {
            "model": settings.ollama_model,
            "messages": messages,
            "stream": stream,
            "options": {"temperature": temperature},
        }
        if stream:
            return self._stream_ollama(url, payload)
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            return resp.json()["message"]["content"]

    async def _stream_ollama(self, url, payload):
        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream("POST", url, json=payload) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                        if content := data.get("message", {}).get("content", ""):
                            yield content
                        if data.get("done"):
                            return
                    except json.JSONDecodeError:
                        continue

    async def _chat_openai(self, messages, stream, temperature):
        response = self._openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=temperature,
            stream=stream,
        )
        if stream:
            return self._stream_openai_compat(response)
        return response.choices[0].message.content

    async def _stream_openai_compat(self, response):
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def _chat_claude(self, messages, stream, temperature):
        system_msg = None
        filtered = []
        for m in messages:
            if m["role"] == "system":
                system_msg = m["content"]
            else:
                filtered.append(m)

        kwargs = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 4096,
            "messages": filtered,
            "temperature": temperature,
        }
        if system_msg:
            kwargs["system"] = system_msg

        if stream:
            return self._stream_claude(kwargs)
        response = self._anthropic_client.messages.create(**kwargs)
        return response.content[0].text

    async def _stream_claude(self, kwargs):
        kwargs["stream"] = True
        with self._anthropic_client.messages.stream(**kwargs) as stream:
            for text in stream.text_stream:
                yield text

    async def _chat_kimi(self, messages, stream, temperature):
        response = self._kimi_client.chat.completions.create(
            model="moonshot-v1-32k",
            messages=messages,
            temperature=temperature,
            stream=stream,
        )
        if stream:
            return self._stream_openai_compat(response)
        return response.choices[0].message.content

    # ── Summarization ────────────────────────────────────────────

    async def summarize_text(self, text: str, file_type: str = "document") -> Dict[str, Any]:
        prompt = f"""Analyze this {file_type} and provide:
1. A concise summary (2-3 sentences)
2. Key topics/keywords (comma-separated)
3. Category (e.g., work, personal, technical, financial, etc.)

Content:
{text[:30000]}

Respond ONLY with valid JSON:
{{"summary": "...", "keywords": "...", "category": "..."}}"""

        try:
            messages = [{"role": "user", "content": prompt}]
            content = await self.chat_completion(messages, stream=False, temperature=0.3)
            result = self._parse_json_response(content)
            return {
                "summary": result.get("summary", ""),
                "keywords": result.get("keywords", ""),
                "category": result.get("category", "unknown"),
                "confidence": 0.9,
                "tokens": self.count_tokens(prompt) + self.count_tokens(str(content)),
                "model": self._current_model_name(),
                "success": True,
            }
        except Exception as e:
            logger.error("Summarization failed: %s", e)
            return {"error": str(e), "success": False}

    async def analyze_image(self, image_path: Path) -> Dict[str, Any]:
        if self.provider in ("yunwu", "openai-compatible") and self._compatible_client:
            return await self._analyze_image_with_compatible(image_path)
        elif self.provider == "claude" and self._anthropic_client:
            return await self._analyze_image_with_claude(image_path)
        elif self.provider == "openai" and self._openai_client:
            return await self._analyze_image_with_openai(image_path)
        elif self.provider == "ollama":
            return await self._analyze_image_with_ollama(image_path)
        return {"error": "No vision-capable provider configured", "success": False}

    async def _analyze_image_with_compatible(self, image_path: Path) -> Dict[str, Any]:
        try:
            model = settings.effective_compatible_model
            with open(image_path, "rb") as f:
                image_data = base64.standard_b64encode(f.read()).decode("utf-8")
            media_type = self._get_media_type(image_path)
            response = self._compatible_client.responses.create(
                model=model,
                input=[{
                    "role": "user",
                    "content": [
                        {"type": "input_image", "image_url": f"data:{media_type};base64,{image_data}"},
                        {"type": "input_text", "text": 'Analyze this image. Respond with JSON: {"summary": "...", "keywords": "...", "category": "..."}'},
                    ],
                }],
                temperature=0.3,
            )
            content = response.output_text
            result = self._parse_json_response(content)
            return {
                "summary": result.get("summary", ""),
                "keywords": result.get("keywords", ""),
                "category": result.get("category", "image"),
                "confidence": 0.9,
                "tokens": getattr(response.usage, "total_tokens", 0) if response.usage else 0,
                "model": model,
                "success": True,
            }
        except Exception as e:
            return {"error": str(e), "success": False}

    async def _analyze_image_with_ollama(self, image_path: Path) -> Dict[str, Any]:
        try:
            with open(image_path, "rb") as f:
                image_b64 = base64.standard_b64encode(f.read()).decode("utf-8")
            url = f"{settings.ollama_host}/api/chat"
            payload = {
                "model": "llava",
                "messages": [{"role": "user", "content": 'Analyze this image. Respond with JSON: {"summary": "...", "keywords": "...", "category": "..."}', "images": [image_b64]}],
                "stream": False,
                "options": {"temperature": 0.3},
            }
            async with httpx.AsyncClient(timeout=120.0) as client:
                resp = await client.post(url, json=payload)
                resp.raise_for_status()
                content = resp.json()["message"]["content"]
                result = self._parse_json_response(content)
                return {"summary": result.get("summary", content[:500]), "keywords": result.get("keywords", ""), "category": result.get("category", "image"), "confidence": 0.85, "tokens": 0, "model": "llava", "success": True}
        except Exception as e:
            return {"error": str(e), "success": False}

    async def _analyze_image_with_claude(self, image_path: Path) -> Dict[str, Any]:
        try:
            with open(image_path, "rb") as f:
                image_data = base64.standard_b64encode(f.read()).decode("utf-8")
            media_type = self._get_media_type(image_path)
            response = self._anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022", max_tokens=1024,
                messages=[{"role": "user", "content": [{"type": "image", "source": {"type": "base64", "media_type": media_type, "data": image_data}}, {"type": "text", "text": 'Analyze this image. Respond with JSON: {"summary": "...", "keywords": "...", "category": "..."}'}]}],
            )
            content = response.content[0].text
            tokens = response.usage.input_tokens + response.usage.output_tokens
            result = self._parse_json_response(content)
            return {"summary": result.get("summary", ""), "keywords": result.get("keywords", ""), "category": result.get("category", "image"), "confidence": 0.9, "tokens": tokens, "model": "claude-3-5-sonnet-20241022", "success": True}
        except Exception as e:
            return {"error": str(e), "success": False}

    async def _analyze_image_with_openai(self, image_path: Path) -> Dict[str, Any]:
        try:
            with open(image_path, "rb") as f:
                image_data = base64.standard_b64encode(f.read()).decode("utf-8")
            media_type = self._get_media_type(image_path)
            response = self._openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": [{"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{image_data}"}}, {"type": "text", "text": 'Analyze this image. Respond with JSON: {"summary": "...", "keywords": "...", "category": "..."}'}]}],
                temperature=0.3,
            )
            content = response.choices[0].message.content
            tokens = response.usage.total_tokens
            result = self._parse_json_response(content)
            return {"summary": result.get("summary", ""), "keywords": result.get("keywords", ""), "category": result.get("category", "image"), "confidence": 0.9, "tokens": tokens, "model": "gpt-4o-mini", "success": True}
        except Exception as e:
            return {"error": str(e), "success": False}

    # ── Embeddings ───────────────────────────────────────────────

    async def get_embedding(self, text: str) -> Optional[List[float]]:
        if self.embedding_provider in ("yunwu", "openai-compatible") and self._compatible_client:
            return await self._get_compatible_embedding(text)
        elif self.embedding_provider == "ollama":
            return await self._get_ollama_embedding(text)
        elif self.embedding_provider == "openai" and self._openai_client:
            return await self._get_openai_embedding(text)
        elif self.embedding_provider == "local" and self._local_embedding_model:
            return self._get_local_embedding(text)
        return None

    async def _get_compatible_embedding(self, text: str) -> Optional[List[float]]:
        try:
            if len(text) > 8000:
                text = text[:8000]
            response = self._compatible_client.embeddings.create(
                model=settings.effective_compatible_embedding_model,
                input=text,
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error("OpenAI-compatible embedding failed: %s", e)
            return None

    async def _get_ollama_embedding(self, text: str) -> Optional[List[float]]:
        try:
            if len(text) > 8000:
                text = text[:8000]
            url = f"{settings.ollama_host}/api/embeddings"
            payload = {"model": settings.ollama_embedding_model, "prompt": text}
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(url, json=payload)
                resp.raise_for_status()
                return resp.json()["embedding"]
        except Exception as e:
            logger.error("Ollama embedding failed: %s", e)
            return None

    async def _get_openai_embedding(self, text: str) -> Optional[List[float]]:
        try:
            if len(text) > 8000:
                text = text[:8000]
            response = self._openai_client.embeddings.create(
                model="text-embedding-3-small", input=text,
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error("OpenAI embedding failed: %s", e)
            return None

    def _get_local_embedding(self, text: str) -> Optional[List[float]]:
        try:
            if len(text) > 2000:
                text = text[:2000]
            embedding = self._local_embedding_model.encode(text, normalize_embeddings=True)
            return embedding.tolist()
        except Exception as e:
            logger.error("Local embedding failed: %s", e)
            return None

    # ── Helpers ───────────────────────────────────────────────────

    def _current_model_name(self) -> str:
        return {
            "yunwu": settings.effective_compatible_model,
            "openai-compatible": settings.effective_compatible_model,
            "ollama": settings.ollama_model,
            "openai": "gpt-4o-mini",
            "claude": "claude-3-5-sonnet-20241022",
            "kimi": "moonshot-v1-32k",
        }.get(self.provider, "unknown")

    @staticmethod
    def _get_media_type(path: Path) -> str:
        return {
            ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".png": "image/png", ".gif": "image/gif",
            ".webp": "image/webp", ".tiff": "image/tiff",
        }.get(path.suffix.lower(), "image/jpeg")

    @staticmethod
    def _parse_json_response(content: str) -> dict:
        try:
            start = content.find("{")
            end = content.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(content[start:end])
        except json.JSONDecodeError:
            pass
        return {"summary": content[:500], "keywords": "", "category": "unknown"}

    async def check_ollama_available(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(f"{settings.ollama_host}/api/tags")
                return resp.status_code == 200
        except Exception:
            return False
