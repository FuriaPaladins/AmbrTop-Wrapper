# AmbrTop-Py
An asynchronous Python API wrapper for ambr.top

## Example

```py
from ambrtop_py import AmbrAPI
import asyncio

async def main():
    api = AmbrAPI()
    all_characters = await api.get_full_characters()
    for character in all_characters:
        print(character.name)
    
    events = await api.get_events()
    for event in events:
        print(f"{event.en.full_name} ends @ {event.ends}")

asyncio.run(main())
```