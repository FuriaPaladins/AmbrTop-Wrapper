from dataclasses import dataclass

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
class EventLang:
    short_name: Optional[str] = None
    full_name: Optional[str] = None
    description: Optional[str] = None
    banner: Optional[str] = None


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