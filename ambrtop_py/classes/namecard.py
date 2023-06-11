from dataclasses import dataclass

from ambrtop_py.classes._functions import *


@dataclass
class Namecard:
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    icon_full: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Namecard':
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        name = from_union([from_str, from_none], obj.get("name"))
        description = from_union([from_str, from_none], obj.get("description"))
        icon = f"https://api.ambr.top/assets/UI/namecard/{obj.get('icon')}.png" if obj.get('icon', None) else None
        icon_full = f"https://api.ambr.top/assets/UI/namecard/{obj.get('icon').replace('_NameCardIcon_', '_NameCardPic_')}_P.png" if obj.get('icon', None) else None
        return Namecard(id, name, description, icon, icon_full)
