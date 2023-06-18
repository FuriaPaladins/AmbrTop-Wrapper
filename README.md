# AmbrTop-Py
An asynchronous Python API wrapper for ambr.top  
*Note: This is my first ever API wrapper I've made publicly available, it may be bad/weird*

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
    
    await api.close()

asyncio.run(main())
```