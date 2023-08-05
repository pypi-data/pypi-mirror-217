"""Example of using the get_objects helper to dump all objects of a given type."""

import argparse
import asyncio
import contextlib
import logging

from aiovantage.config_client import ConfigClient
from aiovantage.config_client.helpers import get_objects

# Grab connection info from command line arguments
parser = argparse.ArgumentParser(description="aiovantage example")
parser.add_argument("host", help="hostname of Vantage controller")
parser.add_argument("--username", help="username for Vantage controller")
parser.add_argument("--password", help="password for Vantage controller")
parser.add_argument("--debug", help="enable debug logging", action="store_true")
args = parser.parse_args()


async def main() -> None:
    """Run code example."""
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    async with ConfigClient(args.host, args.username, args.password) as client:
        # Dump all Areas using the get_objects helper
        print("# Vantage Areas")
        async for area in get_objects(client, types="Area"):
            print(area)
        print()

        # Dump all Loads using the get_objects helper
        print("# Vantage Loads")
        async for load in get_objects(client, types="Load"):
            print(load)
        print()

        # Dump some StationObjects using the get_objects helper
        print("# Vantage Stations")
        async for station in get_objects(client, types=("Keypad", "EqCtrl")):
            print(station)
        print()


with contextlib.suppress(KeyboardInterrupt):
    asyncio.run(main())
