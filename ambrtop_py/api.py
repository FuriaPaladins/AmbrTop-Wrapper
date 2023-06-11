import os.path

import ambrtop_py.api_requests
from ambrtop_py.api_requests import APIRequests
from ambrtop_py.classes.avatar import SmallAvatar, Avatar
from ambrtop_py.classes.misc import DailyDungeons, Event
from ambrtop_py.classes.weapon import WeaponTypes


class AmbrAPI(APIRequests):
    def __init__(self, **kwargs):
        super().__init__(requests_cache=f"{os.path.dirname(ambrtop_py.api_requests.__file__)}/cache", **kwargs)

        self.weapon_types = None

    async def get_characters(self) -> list[SmallAvatar]:
        """
        Get all characters from the avatar endpoint
        Also sets the self.weapon_types variable to the WeaponTypes object
        :return: List of SmallAvatar objects
        """
        _req_ = await self.__make_request__(f'{self.__base_url__}/{self.__language__}/avatar')
        self.weapon_types = WeaponTypes.from_dict(_req_['types'])

        return [SmallAvatar.from_dict(_req_['items'][i], self.weapon_types) for i in _req_['items']]

    async def get_full_characters(self) -> list[Avatar]:
        """
        Get all expanded characters from the avatar endpoint
        Also sets the self.weapon_types variable to the WeaponTypes object
        :return: List of Avatar objects
        """
        _req_ = await self.__make_request__(f'{self.__base_url__}/{self.__language__}/avatar')
        self.weapon_types = WeaponTypes.from_dict(_req_['types'])
        _reqs_ = await self.__make_request__([f'{self.__base_url__}/{self.__language__}/avatar/{i}' for i in _req_['items']])
        return [Avatar.from_dict(i, self.weapon_types) for i in _reqs_]

    async def get_character(self, character_id: int) -> Avatar:
        """
        Get a character from the endpoint: avatar/{character_id}
        :param character_id: The character's ID
        :return: Avatar object
        """
        _req_ = await self.__make_request__(f'{self.__base_url__}/{self.__language__}/avatar/{character_id}')
        return Avatar.from_dict(_req_, self.weapon_types)

    async def 

    async def get_daily_dungeon(self) -> DailyDungeons:
        """
        Get the daily dungeon for all days if day is None
        :return: DailyDungeons object
        """
        _req_ = await self.__make_request__(f'{self.__base_url__}/{self.__language__}/dailyDungeon')
        return DailyDungeons.from_dict(_req_)

    async def get_events(self):
        """
        Get all events
        :return:
        """
        _req_ = await self.__make_request__(f'https://api.ambr.top/assets/data/event.json')
        return [Event.from_dict(_req_[i]) for i in _req_]
