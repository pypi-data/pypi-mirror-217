from random import uniform
import requests
import asyncio


def downloadlinks(
    urls: list | tuple,
    threads: int = 10,
    sleeptime: tuple[int | float, int | float] = (0.01, 0.02),
    verbose: bool = True,
    *args,
    **kwargs,
):
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
    background_tasks = list()
    semaphore = asyncio.Semaphore(threads)

    async def _downloadlinks():
        async def get_with_requests(url, verbose, sleeptime, *args, **kwargs):
            async with semaphore:
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

        for url in urls:
            task = asyncio.create_task(
                get_with_requests(url, verbose, sleeptime, *args, **kwargs)
            )
            background_tasks.append(task)

        return await asyncio.gather(*background_tasks)

    return asyncio.run(_downloadlinks())

