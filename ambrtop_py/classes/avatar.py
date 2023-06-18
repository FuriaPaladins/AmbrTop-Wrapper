from dataclasses import dataclass

import re
from ambrtop_py.api_requests import APIRequests
from ambrtop_py.classes._functions import *
from ambrtop_py.classes.food import SmallFood
from ambrtop_py.classes.misc import AscensionItem, PromoteItem
from ambrtop_py.classes.namecard import Namecard


@dataclass
class SmallAvatar:
    id: Optional[str] = None
    rarity: Optional[int] = None
    name: Optional[str] = None
    element: Optional[str] = None
    weapon_type: Optional[str] = None
    icon: Optional[str] = None
    icon_gacha: Optional[str] = None
    birthday: Optional[List[int]] = None
    release: Optional[int] = None
    route: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any, weapon_types: dict = None) -> 'SmallAvatar':
        assert isinstance(obj, dict)
        id = obj.get("id", None)
        rarity = obj.get("rank", None)
        name = obj.get("name", None)
        element = obj.get("element", None)
        weapon_type = weapon_types.get(obj.get("weaponType", None), None) if weapon_types else obj.get("weaponType", None)
        icon = f"https://api.ambr.top/assets/UI/{obj.get('icon')}.png"
        icon_gacha = f"https://api.ambr.top/assets/UI/{obj.get('icon').replace('UI_AvatarIcon', 'UI_Gacha_AvatarImg')}.png" if obj.get(
            "icon", None) else None
        birthday = obj.get("birthday")
        release = obj.get("release")
        route = obj.get("route")
        return SmallAvatar(id, rarity, name, element, weapon_type, icon, icon_gacha, birthday, release, route)


@dataclass
class VoiceActors:
    en: Optional[str] = None
    chs: Optional[str] = None
    jp: Optional[str] = None
    kr: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'VoiceActors':
        assert isinstance(obj, dict)
        en = obj.get("EN", None)
        chs = obj.get("CHS", None)
        jp = obj.get("JP", None)
        kr = obj.get("KR", None)
        return VoiceActors(en, jp, chs, kr)


@dataclass
class Fetter:
    title: Optional[str] = None
    description: Optional[str] = None
    constellation: Optional[str] = None
    affiliation: Optional[str] = None
    voice_actors: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Fetter':
        assert isinstance(obj, dict)
        title = obj.get("title", None)
        description = obj.get("detail", None)
        constellation = obj.get("constellation", None)
        affiliation = obj.get("native", None)
        voice_actors = VoiceActors.from_dict(obj.get("cv", None)) if obj.get("cv", None) else None
        return Fetter(title, description, constellation, affiliation, voice_actors)


@dataclass
class Costume:
    name: Optional[str] = None
    description: Optional[str] = None
    is_default: Optional[bool] = None
    story_id: Optional[int] = None
    icon: Optional[str] = None
    icon_gacha: Optional[str] = None
    rarity: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Costume':
        assert isinstance(obj, dict)
        name = obj.get("name", None)
        description = obj.get("description", None)
        is_default = obj.get("isDefault", None)
        story_id = obj.get("storyId", None)
        icon = f"https://api.ambr.top/assets/UI/{obj.get('icon')}.png" if obj.get("icon", None) else None
        icon_gacha = f"https://api.ambr.top/assets/UI/{obj.get('icon').replace('_AvatarIcon_', '_Costume_')}.png" if obj.get(
            'icon', None) else None
        rarity = obj.get("rank", None)
        return Costume(name, description, is_default, story_id, icon, icon_gacha, rarity)


@dataclass
class Other:
    costumes: Optional[List[Costume]] = None
    furniture_id: Optional[int] = None
    name_card: Optional[Namecard] = None
    special_dish: Optional[SmallFood] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Other':
        assert isinstance(obj, dict)
        costumes = [Costume.from_dict(x) for x in obj.get("costume", [])] if obj.get("costume", None) else None
        furniture_id = obj.get("furnitureId", None)
        name_card = Namecard.from_dict(obj.get("nameCard", None)) if obj.get("nameCard", None) else None
        special_dish = SmallFood.from_dict(obj.get("specialFood", None)) if obj.get("specialFood", None) else None
        return Other(costumes, furniture_id, name_card, special_dish)


@dataclass
class TalentItem:
    id: Optional[int] = None
    count: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'TalentItem':
        id = int(obj[0])
        count = int(obj[1])
        return TalentItem(id, count)


@dataclass
class TalentPromoteLevel:
    level: Optional[int] = None
    cost_items: Optional[List[TalentItem]] = None
    cost_mora: Optional[int] = None
    description: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'TalentPromoteLevel':
        def format_strings(description_strings, params):
            formatted_strings = []
            for string in description_strings:
                # Find all parameter placeholders in the string
                matches = re.findall(r"{(.*?)}", string)
                for match in matches:
                    if "#" in match:
                        continue
                    # Split the match into its components
                    param_name, param_format = match.split(":")

                    # remove 'param' from the parameter name and subtract 1
                    param_name = int(param_name[5:]) - 1
                    # Get the value of the parameter from the params list
                    param_value = params[param_name]
                    # Format the parameter value according to the specified format
                    if param_format == "F1P":
                        formatted_param = f"{param_value * 100:.1f}%"
                    elif param_format == "F1":
                        formatted_param = f"{param_value:.1f}"
                    elif param_format == "F2":
                        formatted_param = f"{param_value:.2f}%"
                    elif param_format == "P":
                        formatted_param = f"{int(round(param_value * 100, 0))}%"
                    elif param_format == "I":
                        formatted_param = f"{int(round(param_value, 0))}"
                    elif param_format == "F2P":
                        formatted_param = f"{param_value * 100:.2f}%"
                    else:
                        raise ValueError(f"Unknown format: {param_format}")
                    # Replace the parameter placeholder with the formatted value
                    string = string.replace(f"{{{match}}}", formatted_param)
                formatted_strings.append(string)
            return formatted_strings

        assert isinstance(obj, dict)
        level = obj.get("level", None)
        cost_items = [TalentItem(key, item) for key, item in obj.get("costItems", []).items()] if obj.get("costItems",
                                                                                                          None) else None
        cost_mora = obj.get("coinCost", None)
        description = format_strings(obj.get('description'), obj.get('params')) if obj.get("description",
                                                                                           None) else None
        return TalentPromoteLevel(level, cost_items, cost_mora, description)


@dataclass
class AvatarTalent:
    type: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    cooldown: Optional[int] = None
    cost: Optional[int] = None
    levels: Optional[List[TalentPromoteLevel]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'AvatarTalent':
        assert isinstance(obj, dict)
        type = obj.get("type", None)
        name = obj.get("name", None)
        description = obj.get("description", None)
        icon = f"https://api.ambr.top/assets/UI/{obj.get('icon')}.png" if obj.get("icon", None) else None
        cooldown = obj.get("cooldown", None)
        cost = obj.get("cost", None)
        levels = [TalentPromoteLevel.from_dict(obj.get("promote", [])[x]) for x in obj.get("promote", [])] if obj.get(
            "promote", None) else None
        return AvatarTalent(type, name, description, icon, cooldown, cost, levels)

    def get_total_mora_cost(self, start_level=1, end_level=10) -> int:
        """
        Gets the total mora cost of leveling up the talent from start_level to end_level
        :param start_level: level to start counting from
        :param end_level: level to stop counting at
        :return: total mora cost
        """
        if self.levels is None:
            return 0
        total_mora_cost = 0
        for level in self.levels:
            if start_level <= level.level <= end_level:
                total_mora_cost += level.cost_mora if level.cost_mora else 0
        return total_mora_cost


@dataclass
class ExtraConstellationTalentLevel:
    talent_type: Optional[str] = None
    talent_index: Optional[int] = None
    extra_level: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ExtraConstellationTalentLevel':
        assert isinstance(obj, dict)
        talent_type = obj.get("talentType", None)
        talent_index = obj.get("talentIndex", None)
        extra_level = obj.get("extraLevel", None)
        return ExtraConstellationTalentLevel(talent_type, talent_index, extra_level)


@dataclass
class ExtraConstellationData:
    add_talent_extra_level: Optional[List[ExtraConstellationTalentLevel]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ExtraConstellationData':
        assert isinstance(obj, dict)
        add_talent_extra_level = ExtraConstellationTalentLevel.from_dict(obj.get("addTalentExtraLevel", [])) if obj.get(
            "addTalentExtraLevel", None) else None
        return ExtraConstellationData(add_talent_extra_level)


@dataclass
class Constellation:
    name: Optional[str] = None
    description: Optional[str] = None
    extra_data: Optional[ExtraConstellationData] = None
    icon: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Constellation':
        assert isinstance(obj, dict)
        name = obj.get("name", None)
        description = obj.get("description", None)
        extra_data = ExtraConstellationData.from_dict(obj.get("extraData", None)) if obj.get("extraData",
                                                                                             None) else None
        icon = f"https://api.ambr.top/assets/UI/{obj.get('icon')}.png" if obj.get("icon", None) else None
        return Constellation(name, description, extra_data, icon)


@dataclass
class UpgradeProp:
    name: Optional[str] = None
    init_value: Optional[int] = None
    type: Optional[str] = None

    __prop_type__: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any, weapon_types: dict) -> 'UpgradeProp':
        assert isinstance(obj, dict)
        __prop_type__ = obj.get("propType", None)
        name = weapon_types.get(__prop_type__, None)
        init_value = obj.get("initValue", None)
        type = obj.get("type", None)
        return UpgradeProp(name, init_value, type, __prop_type__)


@dataclass
class PromoteLevelProp:
    __prop_type__: Optional[str] = None
    name: Optional[str] = None
    value: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any, weapon_types: dict) -> 'PromoteLevelProp':
        assert isinstance(obj, dict)
        __prop_type__ = obj.get("propType", None)
        name = weapon_types.get(__prop_type__, None)
        value = obj.get("value", None)
        return PromoteLevelProp(__prop_type__, name, value)


@dataclass
class PromoteLevel:
    promote_level: Optional[int] = None
    unlocked_max_level: Optional[int] = None
    item_cost: Optional[List[AscensionItem]] = None
    mora_cost: Optional[int] = None
    required_ar: Optional[int] = None
    add_props: Optional[List[PromoteLevelProp]] = None

    @staticmethod
    def from_dict(obj: Any, weapon_types: dict) -> 'PromoteLevel':
        assert isinstance(obj, dict)
        promote_level = obj.get("promoteLevel", None)
        unlocked_max_level = obj.get("unlockMaxLevel", None)
        item_cost = [PromoteItem.from_dict(x) for x in obj.get("costItems", []).items()] if obj.get("costItems", None) else None
        mora_cost = obj.get("coinCost", None)
        required_ar = obj.get("requiredPlayerLevel", None)
        add_props = [PromoteLevelProp(x, weapon_types.get(x), obj.get("addProps", [])[x]) for x in obj.get("addProps", [])]
        return PromoteLevel(promote_level, unlocked_max_level, item_cost, mora_cost, required_ar, add_props)


@dataclass
class AvatarUpgrade:
    props: Optional[list[UpgradeProp]] = None
    promote: Optional[List[PromoteLevel]] = None

    @staticmethod
    def from_dict(obj: Any, weapon_types: dict) -> 'AvatarUpgrade':
        assert isinstance(obj, dict)
        props = [UpgradeProp.from_dict(x, weapon_types) for x in obj.get("prop", [])]
        promote = [PromoteLevel.from_dict(x, weapon_types) for x in obj.get("promote", [])]
        return AvatarUpgrade(props, promote)



@dataclass()
class Avatar(SmallAvatar):
    fetter: Optional[str] = None
    other: Optional[Other] = None
    ascension: Optional[List[AscensionItem]] = None
    talent: Optional[List[AvatarTalent]] = None
    constellations: Optional[List[Constellation]] = None
    upgrade: Optional[AvatarUpgrade] = None

    @staticmethod
    def from_dict(obj: Any, weapon_types: dict = None) -> 'Avatar':
        assert isinstance(obj, dict)
        id = obj.get("id", None)
        rarity = obj.get("rank", None)
        name = obj.get("name", None)
        element = obj.get("element", None)
        weapon_type = weapon_types.get(obj.get("weaponType", None).replace('WEAPON_SWORD_ONE_HAND', 'WEAPON_SWORD'), None) if weapon_types else None
        icon = f"https://api.ambr.top/assets/UI/{obj.get('icon')}.png"
        icon_gacha = f"https://api.ambr.top/assets/UI/{obj.get('icon').replace('UI_AvatarIcon', 'UI_Gacha_AvatarImg')}.png" if obj.get(
            "icon", None) else None
        birthday = obj.get("birthday")
        release = obj.get("release")
        route = obj.get("route")
        fetter = Fetter.from_dict(obj.get("fetter", None)) if obj.get("fetter", None) else None
        other = Other.from_dict(obj.get("other", None)) if obj.get("other", None) else None
        ascension = [AscensionItem(int(key), int(item)) for key, item in obj.get("ascension", []).items()] if obj.get(
            "ascension") else None
        talent = [AvatarTalent.from_dict(obj.get("talent", [])[x]) for x in obj.get("talent", [])] if obj.get("talent",
                                                                                                              None) else None
        constellations = [Constellation.from_dict(obj.get("constellation", [])[x]) for x in
                          obj.get("constellation", [])] if obj.get("constellation", None) else None

        upgrade = AvatarUpgrade.from_dict(obj.get("upgrade", None), weapon_types) if obj.get("upgrade", None) else None

        return Avatar(id, rarity, name, element, weapon_type, icon, icon_gacha, birthday, release, route, fetter, other,
                      ascension, talent, constellations, upgrade)
