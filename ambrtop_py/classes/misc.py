from dataclasses import dataclass

import bs4

from ambrtop_py.classes._functions import *
import datetime


@dataclass
class Dungeon:
    id: Optional[int] = None
    name: Optional[str] = None
    rewards: Optional[str] = None
    city: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Dungeon':
        assert isinstance(obj, dict)
        id = obj.get("id", None)
        name = obj.get("name", None)
        rewards = obj.get("reward", None)

        ## City numbers to city names
        city = obj.get("city", None)
        city_dicts = {
            1: "Mondstadt",
            2: "Liyue",
            3: "Inazuma",
            4: "Sumeru",
            5: "Fontaine",
            6: "Natlan",
            7: "Snezhnaya",
        }
        city = city_dicts[city]
        return Dungeon(id, name, rewards, city)


@dataclass
class DailyDungeons:
    monday: Optional[list[Dungeon]] = None
    tuesday: Optional[list[Dungeon]] = None
    wednesday: Optional[list[Dungeon]] = None
    thursday: Optional[list[Dungeon]] = None
    friday: Optional[list[Dungeon]] = None
    saturday: Optional[list[Dungeon]] = None
    sunday: Optional[list[Dungeon]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'DailyDungeons':
        assert isinstance(obj, dict)
        monday = [Dungeon.from_dict(obj.get("monday", [])[x]) for x in obj.get("monday", [])]
        tuesday = [Dungeon.from_dict(obj.get("tuesday", [])[x]) for x in obj.get("tuesday", [])]
        wednesday = [Dungeon.from_dict(obj.get("wednesday", [])[x]) for x in obj.get("wednesday", [])]
        thursday = [Dungeon.from_dict(obj.get("thursday", [])[x]) for x in obj.get("thursday", [])]
        friday = [Dungeon.from_dict(obj.get("friday", [])[x]) for x in obj.get("friday", [])]
        saturday = [Dungeon.from_dict(obj.get("saturday", [])[x]) for x in obj.get("saturday", [])]
        sunday = [Dungeon.from_dict(obj.get("sunday", [])[x]) for x in obj.get("sunday", [])]

        return DailyDungeons(monday, tuesday, wednesday, thursday, friday, saturday, sunday)

    # iterable from monday through sunday (not today)
    def __iter__(self):
        return iter([self.monday, self.tuesday, self.wednesday, self.thursday, self.friday, self.saturday, self.sunday])

    # get today
    def get_today(self):
        today = datetime.datetime.today().weekday()
        return list(self)[today]

    # get specific day
    def get_day(self, day: datetime.datetime):
        return list(self)[day.weekday()]


@dataclass
class ParsedEventDescription:
    reward_image: Optional[str] = None
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None
    description: Optional[list[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ParsedEventDescription':
        soup_d = bs4.BeautifulSoup(obj, "lxml")
        reward_image = soup_d.find("img").get('src') if soup_d.find("img") else None
        __times__ = soup_d.find_all("t")
        if len(__times__) >= 2:
            start_time = datetime.datetime.strptime(__times__[0].text, "%Y/%m/%d %H:%M:%S") if __times__[0] else None
            end_time = datetime.datetime.strptime(__times__[1].text, "%Y/%m/%d %H:%M:%S") if __times__[1] else None
        elif len(__times__) == 1:
            end_time = datetime.datetime.strptime(__times__[0].text, "%Y/%m/%d %H:%M:%S") if __times__[0] else None
            start_time = None
        else:
            start_time = None
            end_time = None
        ## Remove the first 6 <p> tags
        for _ in range(6):
            soup_d.p.decompose()
        ## Split lines by <p> tags
        description = [x.text for x in soup_d.find_all("p")]
        # Remove \xa0 and '' from list
        description = [x.replace('\xa0', '') for x in description if x != '\xa0' and x != '']
        ## Remove any \xa0's in each line

        return ParsedEventDescription(reward_image, start_time, end_time, description)


@dataclass
class EventLang:
    short_name: Optional[str] = None
    full_name: Optional[str] = None
    description: Optional[str] = None
    banner: Optional[str] = None
    parsed_description: Optional[ParsedEventDescription] = None

    def __post_init__(self):
        self.parsed_description = ParsedEventDescription.from_dict(self.description)


@dataclass
class Event:
    id: Optional[int] = None
    ends: Optional[datetime.datetime] = None
    en: Optional[EventLang] = None
    ru: Optional[EventLang] = None
    chs: Optional[EventLang] = None
    cht: Optional[EventLang] = None
    kr: Optional[EventLang] = None
    jp: Optional[EventLang] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Event':
        assert isinstance(obj, dict)
        __name__ = obj.get("name", None)
        __name_full__ = obj.get("nameFull", None)
        __description__ = obj.get("description", None)
        __banner__ = obj.get("banner", None)

        id = obj.get("id", None)
        ## Ends at is formatted like: 2023-06-13 17:59:00
        ends = datetime.datetime.strptime(obj.get("endAt"), "%Y-%m-%d %H:%M:%S") if obj.get("endAt", None) else None

        en = EventLang(__name__.get("EN", None), __name_full__.get("EN", None), __description__.get("EN", None), __banner__.get("EN", None))
        ru = EventLang(__name__.get("RU", None), __name_full__.get("RU", None), __description__.get("RU", None), __banner__.get("RU", None))
        chs = EventLang(__name__.get("CHS", None), __name_full__.get("CHS", None), __description__.get("CHS", None), __banner__.get("CHS", None))
        cht = EventLang(__name__.get("CHT", None), __name_full__.get("CHT", None), __description__.get("CHT", None), __banner__.get("CHT", None))
        kr = EventLang(__name__.get("KR", None), __name_full__.get("KR", None), __description__.get("KR", None), __banner__.get("KR", None))
        jp = EventLang(__name__.get("JP", None), __name_full__.get("JP", None), __description__.get("JP", None), __banner__.get("JP", None))

        return Event(id, ends, en, ru, chs, cht, kr, jp)


@dataclass
class AscensionItem:
    id: Optional[int] = None
    level: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AscensionItem':
        id = int(obj[0])
        level = int(obj[1])
        return AscensionItem(id, level)


@dataclass
class PromoteItem:
    id: Optional[int] = None
    count: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'PromoteItem':
        id = int(obj[0])
        count = int(obj[1])
        return PromoteItem(id, count)


@dataclass
class CharacterCurve:
    hp_4star: Optional[int] = None
    attack_4star: Optional[int] = None
    hp_5star: Optional[int] = None
    attack_5star: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'CharacterCurve':
        assert isinstance(obj, dict)
        hp_4star = obj.get("GROW_CURVE_HP_S4", None)
        attack_4star = obj.get("GROW_CURVE_ATTACK_S4", None)
        hp_5star = obj.get("GROW_CURVE_HP_S5", None)
        attack_5star = obj.get("GROW_CURVE_ATTACK_S5", None)
        return CharacterCurve(hp_4star, attack_4star, hp_5star, attack_5star)
