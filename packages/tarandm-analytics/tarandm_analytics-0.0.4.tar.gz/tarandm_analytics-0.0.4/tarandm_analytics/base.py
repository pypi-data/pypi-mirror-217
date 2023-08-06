import asyncio

import aiohttp
import structlog
from aiohttp import ClientSession, ClientTimeout

logger = structlog.get_logger(__name__)


class TaranDMAnalytics:
    def __init__(self, endpoint_url: str, username: str, password: str) -> None:
        self.endpoint_url = endpoint_url + ("" if endpoint_url.endswith("/") else "/")
        self.username = username
        self.password = password

        asyncio.ensure_future(self.validate_url())

    async def validate_url(self) -> None:
        authentication = aiohttp.BasicAuth(login=self.username, password=self.password)

        async with ClientSession(auth=authentication, timeout=ClientTimeout(total=3)) as session:
            url = self.endpoint_url + "info"
            response = await session.get(url=url)

            if response.status == 200:
                logger.info(f"Connection to {self.endpoint_url} was established.")
            elif response.status == 401:
                message = await response.text()
                logger.error(
                    f"Authentication failed. Check that provided credentials are correct. Endpoint message: '{message}'"
                )
