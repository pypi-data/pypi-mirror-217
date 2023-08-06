import asyncio
from random import uniform
import requests


async def get_with_requests(url, verbose, sleeptime, *args, **kwargs):
    """Perform a download using requests.get() with a random sleep time.

    Args:
        url (str): The URL to download.
        verbose (bool): If True, print the progress of each download.
        sleeptime (tuple[int|float, int|float]): A tuple representing the range of random sleep times in seconds before each download.
        *args: Additional positional arguments to pass to the requests.get() function.
        **kwargs: Additional keyword arguments to pass to the requests.get() function.

    Returns:
        A tuple containing the URL and the downloaded data, or None if the download failed.

    """
    if verbose:
        print(f"Downloading: {url}")
    if sleeptime:
        await asyncio.sleep(uniform(*sleeptime))
    data = None
    try:
        with requests.get(url, *args, **kwargs) as res:
            data = res
    except Exception as fe:
        if verbose:
            print(fe)
    return url, data


async def start_all_downloads(urls, semaphore, verbose, sleeptime, *args, **kwargs):
    """Start all downloads with limited concurrency using a semaphore.

    Args:
        urls (list or tuple): A list or tuple of URLs to download.
        semaphore (asyncio.Semaphore): Semaphore to limit the number of concurrent tasks.
        verbose (bool): If True, print the progress of each download.
        sleeptime (tuple[int|float, int|float]): A tuple representing the range of random sleep times in seconds before each download.
        *args: Additional positional arguments to pass to the requests.get() function.
        **kwargs: Additional keyword arguments to pass to the requests.get() function.

    Returns:
        A list of tuples containing the URL and the downloaded data for each successful download.

    """
    results = []
    for url in urls:
        async with semaphore:
            result = await get_with_requests(url, verbose, sleeptime, *args, **kwargs)
            results.append(result)
    return results


def downloadlinks(
    urls: list | tuple,
    threads: int = 10,
    sleeptime: tuple[int | float, int | float] = (0.01, 0.02),
    verbose: bool = True,
    *args,
    **kwargs,
):
    """Download multiple URLs asynchronously using asyncio and requests.

    Args:
        urls (list or tuple): A list or tuple of URLs to download.
        threads (int, optional): The maximum number of concurrent downloads (default: 10).
        sleeptime (tuple[int|float, int|float], optional): A tuple representing the range of random sleep times in seconds before each download (default: (.01, .02)).
        verbose (bool, optional): If True, print the progress of each download (default: True).
        *args: Additional positional arguments to pass to the requests.get() function.
        **kwargs: Additional keyword arguments to pass to the requests.get() function.

    Returns:
        A list of tuples containing the URL and the downloaded data for each successful download.

    """
    semaphore = asyncio.Semaphore(threads)
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(
        start_all_downloads(urls, semaphore, verbose, sleeptime, *args, **kwargs)
    )

