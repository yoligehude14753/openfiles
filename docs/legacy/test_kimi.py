#!/usr/bin/env python3
"""
Test script to verify Kimi API integration
"""
import asyncio
from src.core.config import settings
from src.core.llm_service import LLMService

async def test_kimi():
    print("Testing Kimi API Integration...")
    print(f"Provider: {settings.llm_provider}")
    print(f"Kimi API Key configured: {'Yes' if settings.kimi_api_key else 'No'}")
    print()

    if not settings.kimi_api_key:
        print("❌ KIMI_API_KEY not configured in .env")
        return

    llm_service = LLMService()

    # Test text summarization
    print("1. Testing text summarization...")
    test_text = """
    人工智能（Artificial Intelligence，AI）是计算机科学的一个分支，
    它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。
    该领域的研究包括机器人、语言识别、图像识别、自然语言处理和专家系统等。
    """

    result = await llm_service.summarize_text(test_text, "document")

    if result.get('success'):
        print("✅ Text summarization successful!")
        print(f"   Summary: {result.get('summary')}")
        print(f"   Keywords: {result.get('keywords')}")
        print(f"   Category: {result.get('category')}")
        print(f"   Model: {result.get('model')}")
        print(f"   Tokens: {result.get('tokens')}")
    else:
        print(f"❌ Text summarization failed: {result.get('error')}")

    print()

    # Test embedding (should use OpenAI)
    print("2. Testing embedding generation...")
    embedding = await llm_service.get_embedding("测试文本")

    if embedding:
        print(f"✅ Embedding generation successful! (dimension: {len(embedding)})")
    else:
        print("⚠️  Embedding generation failed (OpenAI API key may not be configured)")

    print()
    print("Test complete!")

if __name__ == "__main__":
    asyncio.run(test_kimi())
