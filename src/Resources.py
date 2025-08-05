"""
# @ Author: FlowDND
# @ Create Time: 2025-08-03 18:48:46
# @ Description: FDRoller is a dice roller for TRPG.
"""

import os
import json


def abspath(path: str) -> str:
    current_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(current_dir, path))
    pass


def loadjson(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as file:
        dictionary = json.load(file)
        pass
    return dictionary
    pass


BACKGROUND_JSON_PATH: str = "../resources/5E/background.json"
BACKGROUND_JSON_PATH: str = abspath(BACKGROUND_JSON_PATH)
BACKGROUND_DICT: dict = loadjson(BACKGROUND_JSON_PATH)

PROFESSION_JSON_PATH: str = "../resources/5E/profession.json"
PROFESSION_JSON_PATH: str = abspath(PROFESSION_JSON_PATH)
PROFESSION_DICT: dict = loadjson(PROFESSION_JSON_PATH)

RACE_JSON_PATH: str = "../resources/5E/race.json"
RACE_JSON_PATH: str = abspath(RACE_JSON_PATH)
RACE_DICT: dict = loadjson(RACE_JSON_PATH)

BASIC_PROPERTY_LIST: list = [
    "力量",
    "敏捷",
    "体质",
    "智力",
    "感知",
    "魅力",
]

SKILLED_PROPERTY_DICT: dict = {
    "体操": "敏捷",
    "驯兽": "感知",
    "奥秘": "智力",
    "运动": "力量",
    "欺瞒": "魅力",
    "历史": "智力",
    "洞察": "感知",
    "威吓": "魅力",
    "调查": "智力",
    "医药": "感知",
    "自然": "智力",
    "察觉": "感知",
    "表演": "魅力",
    "说服": "魅力",
    "宗教": "智力",
    "巧手": "敏捷",
    "隐匿": "敏捷",
    "生存": "感知",
}


def main() -> None:
    print(RACE_DICT)
    pass


if __name__ == "__main__":
    main()
    pass
