import asyncio
import datetime
import os

from aiohttp_client_cache import CachedSession, SQLiteBackend


async def async_print(*args):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, print, *args)


class APIRequests:
    def __init__(self, requests_cache='api_cache', expire_after=None, language='en', debug=False):
        self.__is_debug__ = debug
        self.__expire_after__ = expire_after
        self.__req_cache__ = CachedSession(cache=SQLiteBackend(requests_cache, expire_after=expire_after))
        self.__base_url__ = "https://api.ambr.top/v2"
        self.__language__ = language
        if self.__language__ not in ['en', 'zh', 'ko', 'jp']:
            self.__req_cache__.close()
            raise ValueError("Language must be one of the following: 'en', 'zh', 'ko', 'jp'")

    async def __make_request__(self, url: str | list[str]):
        if isinstance(url, list):
            responses = []
            for url in url:
                async with self.__req_cache__.get(url) as resp:
                    if self.__is_debug__:
                        await async_print(f"{datetime.datetime.now()} DEBUG Requesting: '{url}'")
                    res = await resp.json()
                    if res.get('response') is not None:
                        if res['response'] != 200:
                            raise ValueError(f"Error {res['response']} for {url}")
                        responses.append(res['data'])
                    else:
                        responses.append(res)
            return responses

        async with self.__req_cache__.get(url) as resp:
            if self.__is_debug__:
                await async_print(f"{datetime.datetime.now()} DEBUG Requesting: '{url}'")
            res = await resp.json()
            if res.get('response') is not None:
                if res['response'] != 200:
                    raise ValueError(f"Error {res['response']} for {url}")
                return res['data']
            else:
                return res

    async def clear_cache(self):
        """
        Clear the cache
        :return:
        """
        await async_print(f"{datetime.datetime.now()} DEBUG Clearing cache...")
        await self.__req_cache__.cache.clear()

    async def close(self):
        """
        Close the wrapper
        :return:
        """
        await self.__req_cache__.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
