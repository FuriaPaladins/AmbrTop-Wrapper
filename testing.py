from ambrtop_py import AmbrAPI, Event
import asyncio
import time
from rich import print
import bs4
import html_to_json


async def time_function(func, *args, **kwargs):
    start_time = time.time()
    func_return = await func(*args, **kwargs)
    print(f"Function {func.__name__} {time.time() - start_time} seconds")
    return func_return


async def main():
    start_time = time.time()
    api = AmbrAPI()
    print(f"Took {time.time() - start_time} seconds")

    all_characters = await time_function(api.get_full_characters)
    all_dungeons = await time_function(api.get_daily_dungeon)
    all_weapons = await time_function(api.get_full_weapons)
    events = await time_function(api.get_events)

    print(all_characters[0])
    await api.close()

    # for event in events:
    #    event: Event
    #    print(event.en.short_name)
    #    print(event.en.banner)
    #    # read and pretty print the HTML from event.en.description
    #   print(event.en.parsed_description.reward_image)
    #   print(f"Event Starts: {event.en.parsed_description.start_time} | Event Ends: {event.en.parsed_description.end_time}")
    #    print(event.en.parsed_description.description)
    #   print()


asyncio.run(main())
