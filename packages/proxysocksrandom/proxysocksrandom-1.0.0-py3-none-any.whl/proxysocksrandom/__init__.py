import asyncio
import aiohttp
import random

proxy_links = {
    'https': [
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
        # Добавьте дополнительные ссылки при необходимости
    ],
    'socks5': [
        'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/socks5.txt',
        'https://raw.githubusercontent.com/ALIILAPRO/Proxy/main/socks5.txt',
        'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
        'https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS5_RAW.txt',
        'https://raw.githubusercontent.com/prxchk/proxy-list/main/socks5.txt',
        'https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/main/socks5.txt',
        # Добавьте дополнительные ссылки при необходимости
    ]
}

proxies = {
    'https': [],
    'socks5': []
}


async def fetch_proxies(session, link):
    async with session.get(link) as response:
        if response.status == 200:
            lines = await response.text()
            return lines.split('\n')
    return []


async def update_proxies():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_proxies(session, link) for links in proxy_links.values() for link in links]
        results = await asyncio.gather(*tasks)
        for proxy_type, link_results in zip(proxy_links.keys(), results):
            proxies[proxy_type] = [line for line in link_results if len(line.strip().split(':')) == 2]


def get_random_proxy(proxy_type):
    proxy_list = proxies.get(proxy_type, [])
    random.shuffle(proxy_list)
    return proxy_list[0]


async def periodic_update():
    while True:
        await update_proxies()
        await asyncio.sleep(600)  # Приостановка на 10 минут (600 секунд)


class Proxies:
    def __init__(self):
        self.initialized = False
        self._loop = None

    async def _initialize(self):
        await update_proxies()
        self.initialized = True

    def initialize(self):
        if self.initialized:
            return

        self._loop = asyncio.get_event_loop()
        self._loop.run_until_complete(self._initialize())

    def get_proxy(self, proxy_type):
        if not self.initialized:
            raise RuntimeError("Proxies are not initialized. Call 'initialize' first.")

        if self._loop.is_running():
            return get_random_proxy(proxy_type)
        else:
            return self._loop.run_until_complete(self._get_proxy_async(proxy_type))

    async def _get_proxy_async(self, proxy_type):
        return get_random_proxy(proxy_type)

    async def _update_periodically_async(self):
        if not self.initialized:
            raise RuntimeError("Proxies are not initialized. Call 'initialize' first.")

        await periodic_update()

    def update_periodically(self):
        if self._loop is None:
            raise RuntimeError("Proxies are not initialized. Call 'initialize' first.")

        if self._loop.is_running():
            asyncio.ensure_future(self._update_periodically_async())
        else:
            self._loop.run_until_complete(self._update_periodically_async())
