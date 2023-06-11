from dataclasses import dataclass

from ambrtop_py.classes._functions import *


@dataclass
class WeaponTypes:
    weapon_sword_one_hand: Optional[str] = None
    weapon_claymore: Optional[str] = None
    weapon_bow: Optional[str] = None
    weapon_pole: Optional[str] = None
    weapon_catalyst: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'WeaponTypes':
        assert isinstance(obj, dict)
        weapon_sword_one_hand = from_union([from_str, from_none], obj.get("WEAPON_SWORD_ONE_HAND"))
        weapon_claymore = from_union([from_str, from_none], obj.get("WEAPON_CLAYMORE"))
        weapon_bow = from_union([from_str, from_none], obj.get("WEAPON_BOW"))
        weapon_pole = from_union([from_str, from_none], obj.get("WEAPON_POLE"))
        weapon_catalyst = from_union([from_str, from_none], obj.get("WEAPON_CATALYST"))
        return WeaponTypes(weapon_sword_one_hand, weapon_claymore, weapon_bow, weapon_pole, weapon_catalyst)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.weapon_sword_one_hand is not None:
            result["WEAPON_SWORD_ONE_HAND"] = from_union([from_str, from_none], self.weapon_sword_one_hand)
        if self.weapon_claymore is not None:
            result["WEAPON_CLAYMORE"] = from_union([from_str, from_none], self.weapon_claymore)
        if self.weapon_bow is not None:
            result["WEAPON_BOW"] = from_union([from_str, from_none], self.weapon_bow)
        if self.weapon_pole is not None:
            result["WEAPON_POLE"] = from_union([from_str, from_none], self.weapon_pole)
        if self.weapon_catalyst is not None:
            result["WEAPON_CATALYST"] = from_union([from_str, from_none], self.weapon_catalyst)
        return result
