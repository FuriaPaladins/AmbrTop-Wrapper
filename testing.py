from ambrtop_py import AmbrAPI
import asyncio
import time
from rich import print


async def main():
    start_time = time.time()
    api = AmbrAPI()
    all_characters = await api.get_full_characters()
    all_dungeons = await api.get_daily_dungeon()
    events = await api.get_events()
    for character in all_characters:
        print(character.other.special_dish if character.other else None)
    print(f"Took {time.time() - start_time} seconds")

    await api.close()

asyncio.run(main())
