import asyncio
import os.path

import ambrtop_py.api_requests
from ambrtop_py.api_requests import APIRequests
from ambrtop_py.classes.avatar import SmallAvatar, Avatar
from ambrtop_py.classes.misc import DailyDungeons, Event, UpgradeCurve
from ambrtop_py.classes.monster import SmallMonster, Monster
from ambrtop_py.classes.weapon import SmallWeapon, Weapon


class AmbrAPI(APIRequests):
    def __init__(self, **kwargs):
        super().__init__(requests_cache=f"{os.path.dirname(ambrtop_py.api_requests.__file__)}/cache", **kwargs)

        self.weapon_data = None
        self.monster_types = None

        self.weapon_curve = None
        self.character_curve = None
        self.monster_curve = None

    async def get_characters(self) -> list[SmallAvatar]:
        """
        Get all characters from the avatar endpoint
        Also sets the self.weapon_types variable to the WeaponTypes object
        :return: List of SmallAvatar objects
        """
        _req_ = await self.__make_request__(f'{self.__base_url__}/{self.__language__}/avatar')
        if self.weapon_data is None:
            self.weapon_data = await self.__get_manual_weapon__()
        if self.character_curve is None:
            self.character_curve = await self.__get_character_curve__()
        if self.weapon_curve is None:
            self.weapon_curve = await self.__get_weapon_curve__()
        return [SmallAvatar.from_dict(_req_['items'][i], self.weapon_data) for i in _req_['items']]

    async def get_full_characters(self) -> list[Avatar]:
        """
        Get all expanded characters from the avatar endpoint
        Also sets the self.weapon_types variable to the WeaponTypes object
        :return: List of Avatar objects
        """
        _req_ = await self.__make_request__(f'{self.__base_url__}/{self.__language__}/avatar')
        if self.weapon_data is None:
            self.weapon_data = await self.__get_manual_weapon__()
        if self.character_curve is None:
            self.character_curve = await self.__get_character_curve__()
        if self.weapon_curve is None:
            self.weapon_curve = await self.__get_weapon_curve__()

        _reqs_ = await self.__make_request__([f'{self.__base_url__}/{self.__language__}/avatar/{i}' for i in _req_['items']])
        return [Avatar.from_dict(i, self.weapon_data) for i in _reqs_]

    async def get_character(self, character_id: int) -> Avatar:
        """
        Get a character from the endpoint: avatar/{character_id}
        :param character_id: The character's ID
        :return: Avatar object
        """
        _req_ = await self.__make_request__(f'{self.__base_url__}/{self.__language__}/avatar/{character_id}')
        if self.weapon_data is None:
            self.weapon_data = await self.__get_manual_weapon__()
        if self.character_curve is None:
            self.character_curve = await self.__get_character_curve__()
        if self.weapon_curve is None:
            self.weapon_curve = await self.__get_weapon_curve__()
        return Avatar.from_dict(_req_, self.weapon_data)

    async def get_weapons(self) -> list[SmallWeapon]:
        """
        Get all weapons from the weapon endpoint
        :return: List of SmallWeapon objects
        """
        _req_ = await self.__make_request__(f'{self.__base_url__}/{self.__language__}/weapon')
        if self.weapon_data is None:
            self.weapon_data = await self.__get_manual_weapon__()
        return [SmallWeapon.from_dict(_req_['items'][i], self.weapon_data) for i in _req_['items']]

    async def get_full_weapons(self) -> list[Weapon]:
        """
        Get all expanded weapons from the weapon endpoint
        :return: List of Weapon objects
        """
        _req_ = await self.__make_request__(f'{self.__base_url__}/{self.__language__}/weapon')
        _reqs_ = await self.__make_request__([f'{self.__base_url__}/{self.__language__}/weapon/{i}' for i in _req_['items']])

        return [Weapon.from_dict(i, self.weapon_data) for i in _reqs_]

    async def get_monsters(self):
        """
        Get all monsters from the monster endpoint
        :return:
        """
        _req_ = await self.__make_request__(f'{self.__base_url__}/{self.__language__}/monster')
        if self.monster_types is None:
            self.monster_types = _req_['types']
        if self.monster_curve is None:
            self.monster_curve = await self.__get_monster_curve__()
        return [SmallMonster.from_dict(_req_['items'][i], self.monster_types) for i in _req_['items']]

    async def get_full_monsters(self):
        """
        Get all expanded monsters from the monster endpoint
        :return:
        """
        _req_ = await self.__make_request__(f'{self.__base_url__}/{self.__language__}/monster')
        if self.monster_types is None:
            self.monster_types = _req_['types']
        if self.monster_curve is None:
            self.monster_curve = await self.__get_monster_curve__()
        _reqs_ = await self.__make_request__(
            [f'{self.__base_url__}/{self.__language__}/monster/{i}' for i in _req_['items']])

        _reqs_ = await self.__make_request__([f'{self.__base_url__}/{self.__language__}/monster/{i}' for i in _req_['items']])

        return [Monster.from_dict(i, self.monster_types) for i in _reqs_]

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
        NOTE: Does not cache to keep up to date
        :return:
        """
        _req_ = await self.__make_request__(f'https://api.ambr.top/assets/data/event.json', cache=False)
        return [Event.from_dict(_req_[i]) for i in _req_]

    async def __get_manual_weapon__(self) -> dict:
        """
        Get the weapon data from the manual endpoint
        :return:
        """
        return await self.__make_request__(f'https://api.ambr.top/v2/{self.__language__}/manualWeapon')

    async def __get_character_curve__(self):
        """
        Get the character curve data from the static endpoint
        :return:
        """
        _req_ = await self.__make_request__(f'https://api.ambr.top/v2/static/avatarCurve')
        return [UpgradeCurve.from_dict(_req_[i]) for i in _req_]

    async def __get_weapon_curve__(self):
        """
        Get the weapon curve data from the static endpoint
        :return:
        """
        _req_ = await self.__make_request__(f'https://api.ambr.top/v2/static/weaponCurve')
        return [UpgradeCurve.from_dict(_req_[i]) for i in _req_]

    async def __get_monster_curve__(self):
        """
        Get the monster curve data from the static endpoint
        :return:
        """
        _req_ = await self.__make_request__(f'https://api.ambr.top/v2/static/monsterCurve')
        return [UpgradeCurve.from_dict(_req_[i]) for i in _req_]

    async def fill_cache(self):
        """
        Fill the cache with all data initially so that subsequent requests are faster
        NOTE: This will take quite a while.
        :return: self
        """
        _tasks_ = [asyncio.create_task(i) for i in [self.get_full_characters(), self.get_full_weapons(), self.get_full_monsters(), self.get_daily_dungeon()]]
        await asyncio.gather(*_tasks_)

        return self
