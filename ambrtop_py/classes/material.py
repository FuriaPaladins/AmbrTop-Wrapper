from dataclasses import dataclass

from ambrtop_py.classes._functions import *


@dataclass
class SmallMaterial:
    id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    has_recipe: Optional[bool] = None
    has_map_marker: Optional[bool] = None
    icon: Optional[str] = None
    rarity: Optional[int] = None
    route: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SmallMaterial':
        assert isinstance(obj, dict)
        id = obj.get("id", None)
        name = obj.get("name", None)
        type = obj.get("type", None)
        has_recipe = obj.get("recipe", None)
        has_map_marker = obj.get("mapMark", None)
        icon = f"https://api.ambr.top/assets/UI/{obj.get('icon')}.png" if obj.get("icon", None) else None
        rarity = obj.get("rank", None)
        route = obj.get("route", None)
        return SmallMaterial(id, name, type, has_recipe, has_map_marker, icon, rarity, route)


@dataclass
class MaterialSource:
    name: Optional[str] = None
    type: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'MaterialSource':
        assert isinstance(obj, dict)
        name = obj.get("name", None)
        type = obj.get("type", None)
        return MaterialSource(name, type)


@dataclass
class Material(SmallMaterial):
    description: Optional[str] = None
    source: Optional[List[MaterialSource]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Material':
        assert isinstance(obj, dict)
        id = obj.get("id", None)
        name = obj.get("name", None)
        type = obj.get("type", None)
        has_recipe = obj.get("recipe", None)
        has_map_marker = obj.get("mapMark", None)
        icon = f"https://api.ambr.top/assets/UI/{obj.get('icon')}.png" if obj.get("icon", None) else None
        rarity = obj.get("rank", None)
        route = obj.get("route", None)
        description = obj.get("description", None)
        source = obj.get("source", None)
        return Material(id, name, type, has_recipe, has_map_marker, icon, rarity, route, description, source)
