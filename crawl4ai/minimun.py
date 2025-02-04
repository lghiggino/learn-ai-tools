import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode

async def main():
    browser_config = BrowserConfig(verbose=True)
    run_config = CrawlerRunConfig(
        # Content filtering
        word_count_threshold=10,        # Minimum words per content block
        excluded_tags=[], #Remove tags
        exclude_external_links=True, # Remove external links

        # Content processing
        process_iframes=True,  # Process iframe content
        remove_overlay_elements=True, # Remove popups/modals

        # Cache control
        cache_mode=CacheMode.ENABLED  # Use cache if available
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url="https://www.steamtoy.com.br",
            config=run_config
        )

        if result.success:
            # Print clean content
            print("Content:", result.markdown)  
            markdown = result.markdown
           
            # Process images
            images_array = []
            for image in result.media["images"]:
                images_array.append(image["src"])
                # print(f"Found image: {image['src']}")

            # Process links
            links_array = []
            for link in result.links["internal"]:
                links_array.append(link)
                # print(f"Internal link: {link['href']}")

            print({"md": markdown, "images": images_array, "links": links_array})

        else:
            print(f"Crawl failed: {result.error_message}")

if __name__ == "__main__":
    asyncio.run(main())

    # https://crawl4ai.com/mkdocs/core/crawler-result/