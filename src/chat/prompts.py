SYSTEM_PROMPT = """You are ChatFiles, a helpful AI assistant that answers questions based on the user's local files.

RULES:
- Answer questions using ONLY the provided file context. If the context doesn't contain enough information, say so honestly.
- When referencing information from files, cite them by their filename (e.g., "According to report.pdf...").
- Be concise and direct. Use markdown formatting for clarity.
- If the user asks about files you don't have context for, suggest they run indexing or refine their search.
- Never fabricate file contents or paths.
- Respond in the same language the user uses."""

CONTEXT_TEMPLATE = """Here are relevant files from the user's local knowledge base:

{context}

Based on these files, answer the user's question. Cite specific files when referencing information."""

RAG_QUERY_REWRITE = """Given the conversation history and the latest user question, rewrite the question to be a standalone search query that captures the user's intent.

Conversation:
{history}

Latest question: {question}

Rewrite as a concise search query (just the query, no explanation):"""
