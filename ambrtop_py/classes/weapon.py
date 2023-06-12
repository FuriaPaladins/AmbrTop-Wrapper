from dataclasses import dataclass

from ambrtop_py.classes._functions import *
from ambrtop_py.classes.misc import AscensionItem


@dataclass
class SmallWeapon:
    id: Optional[int] = None
    rarity: Optional[int] = None
    type: Optional[str] = None
    name: Optional[str] = None
    icon: Optional[str] = None
    route: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any, weapon_types: dict = None) -> 'SmallWeapon':
        assert isinstance(obj, dict)
        id = obj.get("id", None)
        rarity = obj.get("rank", None)
        type = weapon_types.get(obj.get("weaponType", None), None) if weapon_types else obj.get("weaponType", None)
        name = obj.get("name", None)
        icon = f"https://api.ambr.top/assets/UI/{obj.get('icon', None)}.png"
        route = obj.get("route", None)
        return SmallWeapon(id, rarity, type, name, icon, route)


@dataclass
class WeaponEffect:
    name: Optional[str] = None
    levels: Optional[list[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'WeaponEffect':
        assert isinstance(obj, dict)
        name = obj.get("name", None)
        __level_data__ = obj.get("upgrade", None)
        levels = [__level_data__[i] for i in __level_data__]
        return WeaponEffect(name, levels)


@dataclass
class Weapon(SmallWeapon):
    story_id: Optional[int] = None
    effect: Optional[WeaponEffect] = None
    description: Optional[str] = None
    ascension: Optional[list[AscensionItem]] = None

    @staticmethod
    def from_dict(obj: Any, weapon_types: dict = None) -> 'Weapon':
        assert isinstance(obj, dict)
        id = obj.get("id", None)
        rarity = obj.get("rank", None)
        type = weapon_types.get(obj.get("weaponType", None), None) if weapon_types else obj.get("weaponType", None)
        name = obj.get("name", None)
        icon = f"https://api.ambr.top/assets/UI/{obj.get('icon', None)}.png"
        route = obj.get("route", None)
        story_id = obj.get("storyId", None)
        effect = WeaponEffect.from_dict([obj.get("affix", None)[i] for i in obj.get("affix", None)][0]) if obj.get("affix", None) else None
        description = obj.get("description", None)
        ascension = [AscensionItem(int(key), int(item)) for key, item in obj.get("ascension", []).items()] if obj.get(
            "ascension") else None
        return Weapon(id, rarity, type, name, icon, route, story_id, effect, description, ascension)