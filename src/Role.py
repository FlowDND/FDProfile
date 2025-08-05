"""
# @ Author: FlowDND
# @ Create Time: 2025-08-03 17:02:23
# @ Description: FDRoller is a dice roller for TRPG.
"""

import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Resources import (
    BACKGROUND_DICT,
    RACE_DICT,
    PROFESSION_DICT,
    SKILLED_PROPERTY_DICT,
    BASIC_PROPERTY_LIST,
)

import json

DEFAULT_USER_JSON_FILE: str = os.path.join(
    os.path.join(os.path.dirname(__file__)), "template.json"
)


def tostr(value: int) -> str:
    if value >= 0:
        return f"+{value}"
    else:
        return str(value)
        pass
    pass


def additionValue(value: int) -> int:
    return (value - 10) // 2
    pass


def strAdditionValue(value: int) -> str:
    value = additionValue(value)
    return tostr(value)
    pass


def proficiencyBonus(level: int) -> int:
    if level <= 4:
        return 2
    elif level <= 8:
        return 3
    elif level <= 12:
        return 4
    elif level <= 16:
        return 5
    elif level <= 20:
        return 6
    else:
        return 7
        pass
    pass


def strProficiencyBonus(level: int) -> str:
    bonus = proficiencyBonus(level)
    return tostr(bonus)
    pass


class Role:

    def __init__(self, config: dict) -> None:
        self.config: dict = config.copy()
        pass

    def markdownBasicInformation(self) -> str:
        text: str = "# 基本信息\n\n"
        text += "---\n\n"
        text += f"- 角色名称: {self.config["基本信息"]["角色名称"]}\n"
        text += f"- 玩家姓名: {self.config["基本信息"]["玩家姓名"]}\n"
        text += f"- 职业: {self.config["基本信息"]["职业"]}\n"
        text += f"- 子职: {self.config["基本信息"]["子职"]}\n"
        text += f"- 种族: {self.config["基本信息"]["种族"]}\n"
        text += f"- 背景: {self.config["基本信息"]["背景"]}\n"
        text += f"- 阵营: {self.config["基本信息"]["阵营"]}\n"
        text += f"- 等级: {self.config["基本信息"]["等级"]}\n"
        text += f"- 主属性: {self.config["基本信息"]["主属性"]}\n"
        return text
        pass

    def markdownProperties(self) -> str:
        text: str = "# 属性\n\n"
        text += "---\n\n"
        text += f"## 基本属性\n\n"
        for property_name in BASIC_PROPERTY_LIST:
            text += f"- {property_name}: {self.config['属性'][property_name]} ({strAdditionValue(self.config['属性'][property_name])})\n"
            pass
        text += "\n---\n"
        text += f"\n## 其他属性\n\n"
        level: int = self.config["基本信息"]["等级"]
        text += f"- 熟练加值: {strProficiencyBonus(level)}\n"
        text += f"- 护甲等级 (AC): {self.config["属性"]["AC"]}\n"
        text += f"- 先攻加值: {strAdditionValue(self.config["属性"]["敏捷"])}\n"
        text += f"- 移动速度: {self.config["属性"]["速度"]}尺\n"
        text += f"- 生命值 (HP): {self.config["属性"]["HP"]}\n"
        text += f"- 生命骰: {self.valueLevel()}d{PROFESSION_DICT[self.strProfession()]["生命值"]}\n"
        feel: int = 10 + self.value("感知")
        if "洞察" in self.config["熟练"]["技能"]:
            feel += self.valueProficiency()
            pass
        text += f"- 被动感知: {feel}\n"
        return text
        pass

    def strProfession(self) -> str:
        return self.config["基本信息"]["职业"]
        pass

    def valueLevel(self) -> int:
        return self.config["基本信息"]["等级"]
        pass

    def valueProficiency(self) -> int:
        return proficiencyBonus(self.valueLevel())
        pass

    def value(self, key: str) -> int:
        return additionValue(self.config["属性"][key])
        pass

    def valueAdditionStrength(self) -> int:
        return additionValue(self.config["属性"]["力量"])
        pass

    def valueAdditionDexterity(self) -> int:
        return additionValue(self.config["属性"]["敏捷"])
        pass

    def valueAdditionConstitution(self) -> int:
        return additionValue(self.config["属性"]["体质"])
        pass

    def valueAdditionIntelligence(self) -> int:
        return additionValue(self.config["属性"]["智力"])
        pass

    def valueAdditionWisdom(self) -> int:
        return additionValue(self.config["属性"]["感知"])
        pass

    def valueAdditionCharisma(self) -> int:
        return additionValue(self.config["属性"]["魅力"])
        pass

    def markdownSkills(self) -> str:
        text: str = f"# 熟练 ({tostr(self.valueProficiency())})\n\n"
        text += "---\n\n"
        text += "## 豁免\n\n"
        for property_name in BASIC_PROPERTY_LIST:
            if property_name in self.config["熟练"]["豁免"]:
                text += f"- [x] {property_name}: {tostr(self.value(property_name) + self.valueProficiency())}\n"
            else:
                text += f"- [ ] {property_name}: {tostr(self.value(property_name))}\n"
                pass
            pass
        text += "\n---\n"
        text += "\n## 技能\n\n"
        for skill, property_name in SKILLED_PROPERTY_DICT.items():
            if skill in self.config["熟练"]["技能"]:
                text += f"- [x] {skill} ({property_name}): {tostr(self.value(property_name) + self.valueProficiency())}\n"
            else:
                text += f"- [ ] {skill} ({property_name}): {tostr(self.value(property_name))}\n"
                pass
            pass
        text += "\n---\n"
        text += "\n## 其他\n\n"
        for others in self.config["熟练"]["其他"]:
            text += f"- {others}\n"
            pass
        return text
        pass

    def markdownProfession(self) -> str:
        text: str = "# 职业\n\n"
        text += f"- 职业: [{self.strProfession()} {PROFESSION_DICT[self.strProfession()]["english"]}]({PROFESSION_DICT[self.strProfession()]["url"]})\n"
        text += f"- 子职: {self.config["基本信息"]["子职"]}\n"
        main_property: str = self.config["基本信息"]["主属性"]
        text += f"- 主属性: {main_property}\n"
        text += f"- 法术 DC: 8 + 熟练 + {main_property}调整值 = {8 + self.value(main_property) + self.valueProficiency()}\n"
        text += f"- 法术攻击加值: 熟练 + {main_property}调整值 = {self.value(main_property) + self.valueProficiency()}\n"
        text += f"\n---\n"
        text += f"\n## 本职特性\n\n"
        for feature, desc in self.config["职业"]["本职"].items():
            text += f"### {feature} ({desc['english']})\n\n"
            text += f"#### 描述\n\n"
            text += f"{desc['描述']}\n\n"
            if "备注" in desc:
                text += f"#### 备注\n\n"
                text += f"{desc['备注']}\n\n"
                pass
            pass
        text += f"\n---\n"
        text += f"\n## 子职特性\n\n"
        for feature, desc in self.config["职业"]["子职"].items():
            text += f"### {feature} ({desc['english']})\n\n"
            text += f"#### 描述\n\n"
            text += f"{desc['描述']}\n\n"
            if "备注" in desc:
                text += f"#### 备注\n\n"
                text += f"{desc['备注']}\n\n"
                pass
            pass
        return text
        pass

    def markdownBelongings(self) -> str:
        text: str = "# 物品\n\n"
        text += "---\n\n"
        for item, desc in self.config["物品"].items():
            text += f"- {item}: {desc}\n"
            pass
        return text
        pass

    def markdownWeapons(self) -> str:
        text: str = "# 武器\n\n"
        text += "---\n\n"
        dataframe: pd.DataFrame = pd.DataFrame(
            columns=["名称", "攻击加值", "伤害", "伤害类型", "范围", "备注"]
        )
        for weapon, desc in self.config["武器"].items():
            property_name: str = desc["属性"]
            attack_bonus: int = self.value(property_name) + self.valueProficiency()
            damage: str = desc["伤害"] + tostr(self.value(property_name))
            dataframe = pd.concat(
                (
                    dataframe,
                    pd.DataFrame(
                        {
                            "名称": [weapon],
                            "攻击加值": [
                                f"熟练 + {property_name}调整值 = " + tostr(attack_bonus)
                            ],
                            "伤害": [damage],
                            "伤害类型": [desc["类型"]],
                            "范围": [desc["范围"]],
                            "备注": [desc["备注"]],
                        },
                        index=[0],
                    ),
                ),
            )
            pass
        # all centered align
        markdown_table: str = dataframe.to_markdown(
            index=False, tablefmt="pipe", colalign=("center",) * 6
        )
        text += markdown_table
        return text
        pass

    def markdownMagic(self) -> str:
        text: str = "# 法术\n\n"
        text += "---\n\n"
        level: int = self.config["基本信息"]["等级"]
        magic_number_list: list = PROFESSION_DICT[self.strProfession()]["法术位"][
            str(level)
        ]
        main_property: str = self.config["基本信息"]["主属性"]
        text += f"- 主属性: {main_property}\n"
        text += f"- 法术 DC: 8 + 熟练 + {main_property}调整值 = {8 + self.value(main_property) + self.valueProficiency()}\n"
        text += f"- 法术攻击加值: 熟练 + {main_property}调整值 = {self.value(main_property) + self.valueProficiency()}\n"
        if "0" in self.config["法术"]:
            text += f"\n---\n"
            text += f"\n## 戏法 (0环法术)\n\n"
            for magic, desc in self.config["法术"]["0"].items():
                text += f"### {magic} ({desc['english']})\n\n"
                text += f"- 系列: {desc['系列']}\n"
                text += f"- 施法时间: {desc['施法时间']}\n"
                text += f"- 范围: {desc['范围']}\n"
                text += f"- 构材: {desc['构材']}\n"
                text += f"- 持续时间: {desc['持续时间']}\n"
                text += f"- 描述时间: {desc['描述']}\n"
                if "备注" in desc:
                    text += f"- 备注: {desc['备注']}\n"
                    pass
                text += "\n"
                pass
            pass
        for i in range(len(magic_number_list)):
            if str(i + 1) not in self.config["法术"]:
                continue
                pass
            text += f"\n---\n"
            text += f"\n## {i + 1}级法术位 ({magic_number_list[i]})\n\n"
            for magic, desc in self.config["法术"][str(i + 1)].items():
                text += f"### {magic} ({desc['english']})\n\n"
                text += f"- 系列: {desc['系列']}\n"
                text += f"- 施法时间: {desc['施法时间']}\n"
                text += f"- 范围: {desc['范围']}\n"
                text += f"- 构材: {desc['构材']}\n"
                text += f"- 持续时间: {desc['持续时间']}\n"
                text += f"- 描述时间: {desc['描述']}\n"
                if "备注" in desc:
                    text += f"- 备注: {desc['备注']}\n"
                    pass
                text += "\n"
                pass
            pass
        return text
        pass

    def markdownStory(self) -> str:
        text: str = "# 冒险故事\n\n"
        for story, desc in self.config["冒险故事"].items():
            text += f"\n---\n\n"
            text += f"## {story}\n\n"
            text += f"{desc}\n"
            pass
        return text
        pass

    def markdownNotes(self) -> str:
        text: str = "# 旅行笔记\n\n"
        for note, desc in self.config["旅行笔记"].items():
            text += f"\n---\n\n"
            text += f"## {note}\n\n"
            text += f"{desc}\n"
            pass
        return text
        pass

    def markdownPersonalInformation(self) -> str:
        text: str = "# 个人信息\n\n"
        text += self.config["个人笔记"]
        return text
        pass

    def markdownRace(self) -> str:
        text: str = "# 种族\n"
        race: str = self.config["基本信息"]["种族"]
        text += f"\n---\n\n"
        text += (
            f"- 种族: [{race} {RACE_DICT[race]["english"]}]({RACE_DICT[race]["url"]})\n"
        )
        for character, desc in RACE_DICT[race]["character"].items():
            text += f"- {character}: {desc}\n"
            pass
        for feature, desc in RACE_DICT[race]["description"].items():
            text += f"\n---\n\n"
            text += f"## {feature}\n\n"
            text += f"{desc}\n"
            pass
        return text
        pass

    def markdownBackground(self) -> str:
        text: str = "# 背景\n"
        background: str = self.config["基本信息"]["背景"]
        text += f"\n---\n\n"
        text += f"- 背景: [{background} {BACKGROUND_DICT[background]["english"]}]({BACKGROUND_DICT[background]["url"]})\n"
        for character, desc in BACKGROUND_DICT[background]["description"].items():
            text += f"- {character}: {desc}\n"
            pass
        return text
        pass

    pass


def main() -> None:
    with open(DEFAULT_USER_JSON_FILE, "r", encoding="utf-8") as file:
        config: dict = json.load(file)
        pass
    role = Role(config)
    TEST_FOLDER: str = "drafts/test"
    if not os.path.exists(TEST_FOLDER):
        os.makedirs(TEST_FOLDER)
        pass
    with open(os.path.join(TEST_FOLDER, "basicinfo.md"), "w", encoding="utf-8") as file:
        file.write(role.markdownBasicInformation())
        pass
    with open(
        os.path.join(TEST_FOLDER, "properties.md"), "w", encoding="utf-8"
    ) as file:
        file.write(role.markdownProperties())
        pass
    with open(os.path.join(TEST_FOLDER, "skills.md"), "w", encoding="utf-8") as file:
        file.write(role.markdownSkills())
        pass
    with open(
        os.path.join(TEST_FOLDER, "professions.md"), "w", encoding="utf-8"
    ) as file:
        file.write(role.markdownProfession())
        pass
    with open(
        os.path.join(TEST_FOLDER, "belongings.md"), "w", encoding="utf-8"
    ) as file:
        file.write(role.markdownBelongings())
        pass
    with open(os.path.join(TEST_FOLDER, "weapons.md"), "w", encoding="utf-8") as file:
        file.write(role.markdownWeapons())
        pass
    with open(os.path.join(TEST_FOLDER, "magic.md"), "w", encoding="utf-8") as file:
        file.write(role.markdownMagic())
        pass
    with open(os.path.join(TEST_FOLDER, "story.md"), "w", encoding="utf-8") as file:
        file.write(role.markdownStory())
        pass
    with open(os.path.join(TEST_FOLDER, "notes.md"), "w", encoding="utf-8") as file:
        file.write(role.markdownNotes())
        pass
    with open(
        os.path.join(TEST_FOLDER, "personalinfo.md"), "w", encoding="utf-8"
    ) as file:
        file.write(role.markdownPersonalInformation())
        pass
    with open(os.path.join(TEST_FOLDER, "race.md"), "w", encoding="utf-8") as file:
        file.write(role.markdownRace())
        pass
    with open(
        os.path.join(TEST_FOLDER, "background.md"), "w", encoding="utf-8"
    ) as file:
        file.write(role.markdownBackground())
        pass
    pass


if __name__ == "__main__":
    main()
    pass
