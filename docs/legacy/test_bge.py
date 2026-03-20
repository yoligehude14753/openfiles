#!/usr/bin/env python3
"""
Test script to verify BGE local embedding integration
"""
import asyncio
from src.core.config import settings
from src.core.llm_service import LLMService

async def test_bge():
    print("Testing BGE Local Embedding Integration...")
    print(f"Embedding Provider: {settings.embedding_provider}")
    print(f"Embedding Model: {settings.embedding_model}")
    print()

    llm_service = LLMService()

    # Test 1: Generate embedding for Chinese text
    print("1. Testing Chinese text embedding...")
    text_cn = "人工智能技术在文档检索中的应用"
    embedding_cn = await llm_service.get_embedding(text_cn)

    if embedding_cn:
        print(f"✅ Chinese embedding successful!")
        print(f"   Dimension: {len(embedding_cn)}")
        print(f"   Sample values: {embedding_cn[:5]}")
    else:
        print("❌ Chinese embedding failed")

    print()

    # Test 2: Generate embedding for English text
    print("2. Testing English text embedding...")
    text_en = "Artificial intelligence application in document retrieval"
    embedding_en = await llm_service.get_embedding(text_en)

    if embedding_en:
        print(f"✅ English embedding successful!")
        print(f"   Dimension: {len(embedding_en)}")
        print(f"   Sample values: {embedding_en[:5]}")
    else:
        print("❌ English embedding failed")

    print()

    # Test 3: Similarity test
    if embedding_cn and embedding_en:
        print("3. Testing semantic similarity...")

        # Similar texts
        text1 = "预算报告"
        text2 = "财务规划"
        text3 = "技术文档"

        emb1 = await llm_service.get_embedding(text1)
        emb2 = await llm_service.get_embedding(text2)
        emb3 = await llm_service.get_embedding(text3)

        # Calculate cosine similarity
        def cosine_similarity(a, b):
            dot_product = sum(x * y for x, y in zip(a, b))
            magnitude_a = sum(x * x for x in a) ** 0.5
            magnitude_b = sum(y * y for y in b) ** 0.5
            return dot_product / (magnitude_a * magnitude_b)

        sim_12 = cosine_similarity(emb1, emb2)
        sim_13 = cosine_similarity(emb1, emb3)

        print(f"   Similarity('预算报告', '财务规划'): {sim_12:.4f}")
        print(f"   Similarity('预算报告', '技术文档'): {sim_13:.4f}")

        if sim_12 > sim_13:
            print("   ✅ Semantic similarity works correctly!")
            print("      (预算报告 更接近 财务规划，而不是 技术文档)")
        else:
            print("   ⚠️  Unexpected similarity results")

    print()
    print("Test complete!")

if __name__ == "__main__":
    asyncio.run(test_bge())
