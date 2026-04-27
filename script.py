import asyncio
import aiohttp
import logging
from typing import List, Dict, Any
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)


async def get_data() -> List[Dict[str, Any]]:
    """
    Fetch data from multiple URLs asynchronously.
    
    Returns:
        List of dictionaries containing the fetched data.
    """
    data: List[Dict[str, Any]] = []
    urls: List[str] = [
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/posts/2",
        "https://jsonplaceholder.typicode.com/posts/3"
    ]

    logger.info(f"Starting to fetch data from {len(urls)} URLs")
    
    try:
        async with aiohttp.ClientSession() as session:
            for url in urls:
                try:
                    logger.debug(f"Fetching data from: {url}")
                    async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                        if response.status == 200:
                            json_data: Dict[str, Any] = await response.json()
                            data.append(json_data)
                            logger.info(f"Successfully fetched data from {url}")
                        else:
                            logger.error(f"Failed to fetch from {url}: HTTP {response.status}")
                except asyncio.TimeoutError:
                    logger.error(f"Timeout while fetching from {url}")
                except aiohttp.ClientError as e:
                    logger.error(f"Network error while fetching from {url}: {e}")
                except Exception as e:
                    logger.error(f"Unexpected error while fetching from {url}: {e}")
                
                await asyncio.sleep(1)
    except Exception as e:
        logger.error(f"Failed to create client session: {e}")
        raise

    logger.info(f"Completed fetching. Retrieved {len(data)} successful responses")
    return data


def process_data(data: List[Dict[str, Any]]) -> List[str]:
    """
    Process fetched data and extract titles.
    
    Args:
        data: List of dictionaries containing the fetched data.
    
    Returns:
        List of titles extracted from the data.
    """
    result: List[str] = []
    logger.info(f"Processing {len(data)} items")
    
    try:
        for item in data:
            if "title" in item and isinstance(item["title"], str):
                result.append(item["title"])
        logger.info(f"Processed data: extracted {len(result)} titles")
    except Exception as e:
        logger.error(f"Error during data processing: {e}")
        raise

    return result


async def main() -> None:
    """Main entry point for the application."""
    try:
        logger.info("Application started")
        data: List[Dict[str, Any]] = await get_data()
        titles: List[str] = process_data(data)
        print(titles)
        logger.info("Application completed successfully")
    except Exception as e:
        logger.error(f"Application failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())