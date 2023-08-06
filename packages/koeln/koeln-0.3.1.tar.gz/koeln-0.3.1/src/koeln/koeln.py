"""Asynchronous Python client providing Open Data information of Köln."""
from __future__ import annotations

import asyncio
import socket
from dataclasses import dataclass
from importlib import metadata
from typing import Any, cast

import async_timeout
from aiohttp import ClientError, ClientSession
from aiohttp.hdrs import METH_GET
from yarl import URL

from .exceptions import ODPKoelnConnectionError, ODPKoelnError
from .models import DisabledParking


@dataclass
class ODPKoeln:
    """Main class for handling data fetchting from Open Data Platform of Köln."""

    request_timeout: float = 10.0
    session: ClientSession | None = None

    _close_session: bool = False

    async def _request(
        self,
        uri: str,
        *,
        method: str = METH_GET,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Handle a request to the Open Data Platform API of Köln.

        Args:
        ----
            uri: Request URI, without '/', for example, 'status'
            method: HTTP method to use, for example, 'GET'
            params: Extra options to improve or limit the response.

        Returns:
        -------
            A Python dictionary (text) with the response from
            the Open Data Platform API of Köln.

        Raises:
        ------
            ODPKoelnConnectionError: Timeout occurred while
                connecting to the Open Data Platform API.
            ODPKoelnError: If the data is not valid.
        """
        version = metadata.version(__package__)
        url = URL.build(
            scheme="https",
            host="offenedaten-koeln.de",
            path="/api/action/datastore/",
        ).join(URL(uri))

        headers = {
            "Accept": "application/json",
            "User-Agent": f"PythonODPKoeln/{version}",
        }

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self.session.request(
                    method,
                    url,
                    params=params,
                    headers=headers,
                    ssl=True,
                )
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            msg = "Timeout occurred while connecting to the Open Data Platform API."
            raise ODPKoelnConnectionError(
                msg,
            ) from exception
        except (ClientError, socket.gaierror) as exception:
            msg = "Error occurred while communicating with Open Data Platform API."
            raise ODPKoelnConnectionError(
                msg,
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            msg = "Unexpected content type response from the Open Data Platform API"
            raise ODPKoelnError(
                msg,
                {"Content-Type": content_type, "Response": text},
            )

        return cast(dict[str, Any], await response.json())

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> ODPKoeln:
        """Async enter.

        Returns
        -------
            The Open Data Platform Koeln object.
        """
        return self

    async def __aexit__(self, *_exc_info: Any) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.
        """
        await self.close()


@dataclass
class StadtKoeln:
    """Main class for handling data fetchting from Stadt of Köln."""

    request_timeout: float = 10.0
    session: ClientSession | None = None

    _close_session: bool = False

    async def _request(
        self,
        uri: str,
        *,
        method: str = METH_GET,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Handle a request to the Stadt of Köln API.

        Args:
        ----
            uri: Request URI, without '/', for example, 'status'
            method: HTTP method to use, for example, 'GET'
            params: Extra options to improve or limit the response.

        Returns:
        -------
            A Python dictionary (text) with the response from
            the Open Data Platform API of Koeln.

        Raises:
        ------
            ODPKoelnConnectionError: Timeout occurred while
                connecting to the Open Data Platform API.
            ODPKoelnError: If the data is not valid.
        """
        version = metadata.version(__package__)
        url = URL.build(
            scheme="https",
            host="geoportal.stadt-koeln.de",
            path="/arcgis/rest/services/",
        ).join(URL(uri))

        headers = {
            "Accept": "application/json",
            "User-Agent": f"PythonStadtKoeln/{version}",
        }

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self.session.request(
                    method,
                    url,
                    params=params,
                    headers=headers,
                    ssl=True,
                )
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            msg = "Timeout occurred while connecting to the Open Data Platform API."
            raise ODPKoelnConnectionError(
                msg,
            ) from exception
        except (ClientError, socket.gaierror) as exception:
            msg = "Error occurred while communicating with Open Data Platform API."
            raise ODPKoelnConnectionError(
                msg,
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            msg = "Unexpected content type response from the Open Data Platform API"
            raise ODPKoelnError(
                msg,
                {"Content-Type": content_type, "Response": text},
            )

        return cast(dict[str, Any], await response.json())

    async def disabled_parkings(self) -> list[DisabledParking]:
        """Get list of disabled parking spaces.

        Returns
        -------
            A list of DisabledParking objects.
        """
        locations = await self._request(
            "basiskarten/stadtplanthemen/MapServer/0/query",
            params={
                "where": "objectid is not null",
                "outFields": "*",
                "outSR": "4326",
                "f": "json",
            },
        )
        return [DisabledParking.from_dict(item) for item in locations["features"]]

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> StadtKoeln:
        """Async enter.

        Returns
        -------
            The Stadt Koeln object.
        """
        return self

    async def __aexit__(self, *_exc_info: Any) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.
        """
        await self.close()
