from dataclasses import dataclass
from typing import Optional


@dataclass
class SmallMonster:
    id: Optional[int] = None
    name: Optional[str] = None
    type: Optional[str] = None
    icon: Optional[str] = None
    route: Optional[str] = None

    @staticmethod
    def from_dict(obj: dict, monster_types: dict = None) -> 'SmallMonster':
        assert isinstance(obj, dict)
        id = obj.get("id", None)
        name = obj.get("name", None)
        type = monster_types.get(obj.get("type", None), None)
        icon = f"https://api.ambr.top/assets/UI/monster/{obj.get('icon', None)}.png"
        route = obj.get("route", None)
        return SmallMonster(id, name, type, icon, route)


@dataclass
class MonsterTip:
    id: Optional[int] = None
    images: Optional[list[str]] = None
    description: Optional[str] = None



@dataclass
class Monster(SmallMonster):
    title: Optional[str] = None
    special_name: Optional[str] = None
    description: Optional[str] = None
    tips: Optional[list[MonsterTip]] = None

    @staticmethod
    def from_dict(obj: dict, monster_types: dict = None) -> 'Monster':
        assert isinstance(obj, dict)
        id = obj.get("id", None)
        name = obj.get("name", None)
        type = monster_types.get(obj.get("type", None), None)
        icon = f"https://api.ambr.top/assets/UI/monster/{obj.get('icon', None)}.png"
        route = obj.get("route", None)
        title = obj.get("title", None)
        special_name = obj.get("specialName", None)
        description = obj.get("description", None)
        tips = [MonsterTip(int(i), [f"https://api.ambr.top/assets/UI/tutorial/{tip_img}{'.png' if '.png' not in tip_img else ''}" for tip_img in obj.get('tips', None)[i]['images']], obj.get('tips', None)[i]['description']) for i in obj.get("tips", None)] if obj.get("tips", None) else None
        return Monster(id, name, type, icon, route, title, special_name, description, tips)
