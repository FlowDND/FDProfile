"""
# @ Author: FlowDND
# @ Create Time: 2025-08-03 15:37:21
# @ Description: FDRoller is a dice roller for TRPG.
"""

import os
import json

GROUPS_PATH: str = "data/Groups"
GROUP_LIST: list[str] = os.listdir(GROUPS_PATH)
GROUP_PATH_DICT: dict[str, str] = {
    group: os.path.join(os.path.abspath(GROUPS_PATH), group) for group in GROUP_LIST
}
DEFAULT_USER_JSON_FILE: str = os.path.join(
    os.path.join(os.path.dirname(__file__)), "template.json"
)


def check(group_name: str, user: str) -> tuple[bool, str]:
    user_json_file: str = os.path.join(
        GROUP_PATH_DICT[group_name], f"{user}", f"{user}.json"
    )
    if not os.path.exists(user_json_file):
        return False, "wrong."
        pass
    else:
        return True, user_json_file
        pass
    pass


if __name__ == "__main__":
    print("Available groups:")
    for group in GROUP_LIST:
        print(f"- {group}")
        pass
    for group, path in GROUP_PATH_DICT.items():
        print(f"  {group}: {path}")
        pass
    with open(DEFAULT_USER_JSON_FILE, "r", encoding="utf-8") as DEFAULT_USER_JSON_FILE:
        json_dict: dict = json.load(DEFAULT_USER_JSON_FILE)
        pass
    print(f"Default user JSON template: {json_dict}")
    pass
