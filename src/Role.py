"""
# @ Author: FlowDND
# @ Create Time: 2025-08-03 17:02:23
# @ Description: FDRoller is a dice roller for TRPG.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Resources import BACKGROUND_DICT, RACE_DICT, PROFESSION_DICT, SKILLED_PROPERTY_DICT

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
        return text
        pass

    def markdownProperties(self) -> str:
        text: str = "# 属性\n\n"
        text += "---\n\n"
        text += f"## 基本属性\n\n"
        text += f"- 力量: {self.config["属性"]["力量"]} ({strAdditionValue(self.config["属性"]["力量"])})\n"
        text += f"- 敏捷: {self.config["属性"]["敏捷"]} ({strAdditionValue(self.config["属性"]["敏捷"])})\n"
        text += f"- 体质: {self.config["属性"]["体质"]} ({strAdditionValue(self.config["属性"]["体质"])})\n"
        text += f"- 智力: {self.config["属性"]["智力"]} ({strAdditionValue(self.config["属性"]["智力"])})\n"
        text += f"- 感知: {self.config["属性"]["感知"]} ({strAdditionValue(self.config["属性"]["感知"])})\n"
        text += f"- 魅力: {self.config["属性"]["魅力"]} ({strAdditionValue(self.config["属性"]["魅力"])})\n"
        text += "\n---\n"
        text += f"\n## 其他属性\n\n"
        level: int = self.config["基本信息"]["等级"]
        text += f"- 熟练加值: {strProficiencyBonus(level)}\n"
        text += f"- 护甲等级 (AC): {self.config["属性"]["AC"]}\n"
        text += f"- 先攻加值: {strAdditionValue(self.config["属性"]["敏捷"])}\n"
        text += f"- 移动速度: {self.config["属性"]["速度"]}尺\n"
        text += f"- 生命值 (HP): {self.config["属性"]["HP"]}\n"
        text += f"- 生命骰: "
        return text
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
        for value in self.config["熟练"]["豁免"]:
            text += f"- {value}: {tostr(self.value(value) + self.valueProficiency())}\n"
            pass
        text += "\n---\n"
        text += "\n## 技能\n\n"
        for value in self.config["熟练"]["技能"]:
            character: str = SKILLED_PROPERTY_DICT[value]
            text += f"- {value}({character}): {tostr(self.value(character) + self.valueProficiency())}\n"
            pass
        return text
        pass

    def markdownJob(self) -> str:
        text: str = "# 职业\n\n"
        text += "---\n\n"
        text += f"- 职业: {self.config["基本信息"]["职业"]}\n"
        text += f"- 子职: {self.config["基本信息"]["子职"]}\n"
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
    with open(
        os.path.join(TEST_FOLDER, "basic_info.md"), "w", encoding="utf-8"
    ) as file:
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
    with open(os.path.join(TEST_FOLDER, "job.md"), "w", encoding="utf-8") as file:
        file.write(role.markdownJob())
        pass
    pass


if __name__ == "__main__":
    main()
    pass
