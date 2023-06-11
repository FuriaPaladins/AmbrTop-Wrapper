from ambrtop_py.classes._functions import *
from dataclasses import dataclass


@dataclass
class SmallFood:
    id: Optional[str] = None
    name: Optional[str] = None
    rarity: Optional[int] = None
    effect_icon: Optional[str] = None
    icon: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'SmallFood':
        assert isinstance(obj, dict)
        id = obj.get("id", None)
        name = obj.get("name", None)
        rarity = obj.get("rank", None)
        effect_icon = f"https://api.ambr.top/assets/UI/{obj.get('effectIcon')}.png" if obj.get('effectIcon', None) else None
        icon = f"https://api.ambr.top/assets/UI/{obj.get('icon')}.png" if obj.get('icon', None) else None
        return SmallFood(id, name, rarity, effect_icon, icon)
