import os
import asyncio
import json
from pydantic import BaseModel, Field
from typing import List
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import LLMExtractionStrategy

class Product(BaseModel):
    name: str
    price: str
    linkUrl: str
    imageUrl: str

async def main():
    # 1. Define the LLM extraction strategy
    llm_strategy = LLMExtractionStrategy(
        provider="openai/gpt-4o-mini",            # e.g. "ollama/llama2"
        api_token=os.getenv('OPENAI_API_KEY'),
        schema=Product.model_json_schema(),            # Or use model_json_schema()
        extraction_type="schema",
        instruction="""Thoroughly scan the entire webpage content, including any dynamically loaded or hidden sections. Extract every product object that contains the keys 'name', 'price', 'linkUrl', and 'imageUrl'. 
        Return all of these product objects in a JSON array format, ensuring that no product is missed. Do not add anymore fields then the ones mentioned""",
        chunk_token_threshold=1000,
        overlap_rate=0.1,
        apply_chunking=True,
        input_format="markdown",   # or "html", "fit_markdown"
        extra_args={"temperature": 0.0, "max_tokens": 10000}
    )

    # 2. Build the crawler config
    crawl_config = CrawlerRunConfig(
        extraction_strategy=llm_strategy,
        cache_mode=CacheMode.BYPASS
    )

    # 3. Create a browser config if needed
    browser_cfg = BrowserConfig(headless=False)

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        # 4. Let's say we want to crawl a single page
        result = await crawler.arun(
            url="https://www.samsonite.com.br",
            config=crawl_config
        )

        if result.success:
            # 5. The extracted content is presumably JSON
            data = json.loads(result.extracted_content)
            print("Extracted items:", data)

            # 6. Show usage stats
            llm_strategy.show_usage()  # prints token usage
        else:
            print("Error:", result.error_message)

if __name__ == "__main__":
    asyncio.run(main())