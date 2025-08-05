"""
# @ Author: FlowDND
# @ Create Time: 2025-08-03 15:26:37
# @ Description: FDRoller is a dice roller for TRPG.
"""

import os
import sys
import json
from collections import OrderedDict
import streamlit as st

sys.path.append(os.path.dirname(__file__))

from Login import check
from Role import Role

LOGO_IMAGE_PATH: str = "resources/images/dnd_logo.png"

# login page


def loginPage() -> OrderedDict:
    st.title("FlowDND 龙与地下城角色管理")
    st.write("欢迎来到 FlowDND 剑与魔法的世界！")
    # group name
    group_name = st.text_input("冒险队", "")
    # user name
    user_name = st.text_input("用户名", "")
    # password
    password = st.text_input("密码", "", type="password")
    # login button
    if st.button("登录"):
        if group_name and user_name and password:
            success, message = check(group_name, user_name, password)
            if success:
                with open(message, "r", encoding="utf-8") as user_json:
                    user_config: OrderedDict = json.load(
                        user_json, object_pairs_hook=OrderedDict
                    )
                    pass
                profession = user_config["基本信息"]["职业"]
                subprofession = user_config["基本信息"]["子职"]
                name: str = user_config["基本信息"]["角色名称"]
                st.success(
                    f"登录成功! 欢迎回来, {user_name}!  来自 {group_name} 冒险队的 {profession} - {subprofession} {name}!"
                )
                st.session_state["user_json_file"] = message
                st.session_state["group_name"] = group_name
                return user_config
                pass
            else:
                st.error(message)
                pass
        else:
            st.warning("请填写所有字段。")
            pass
        pass
    st.image(LOGO_IMAGE_PATH, use_container_width=True)
    pass


FUNCTION_DICT: dict = {
    "基本信息": lambda role: role.markdownBasicInformation(),
    "属性": lambda role: role.markdownProperties(),
    "熟练": lambda role: role.markdownSkills(),
    "种族": lambda role: role.markdownRace(),
    "背景": lambda role: role.markdownBackground(),
    "职业": lambda role: role.markdownProfession(),
    "物品": lambda role: role.markdownBelongings(),
    "武器": lambda role: role.markdownWeapons(),
    "法术": lambda role: role.markdownMagic(),
    "冒险故事": lambda role: role.markdownStory(),
    "旅行笔记": lambda role: role.markdownNotes(),
    "个人信息": lambda role: role.markdownPersonalInformation(),
}

# 可编辑的部分
EDITABLE_SECTIONS = ["旅行笔记", "个人信息"]


def save_user_data():
    """保存用户数据到JSON文件"""
    if "user_config" in st.session_state and "user_json_file" in st.session_state:
        with open(st.session_state.user_json_file, "w", encoding="utf-8") as f:
            json.dump(st.session_state.user_config, f, ensure_ascii=False, indent=4)
        st.success("✅ 保存成功！")


def edit_notes(role: Role):
    """编辑旅行笔记"""
    st.title("📝 编辑旅行笔记")

    notes = st.session_state.user_config["旅行笔记"]

    # 显示现有笔记
    if notes:
        st.subheader("📖 现有笔记")
        for note_title, note_content in notes.items():
            with st.expander(f"📄 {note_title}"):
                st.write(note_content)

    # 编辑现有笔记
    if notes:
        st.subheader("✏️ 编辑现有笔记")
        selected_note = st.selectbox("选择要编辑的笔记", list(notes.keys()))

        if selected_note:
            edited_title = st.text_input(
                "编辑标题", value=selected_note, key="edit_note_title"
            )
            edited_content = st.text_area(
                "编辑内容",
                value=notes[selected_note],
                height=200,
                key="edit_note_content",
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 保存修改"):
                    if edited_title and edited_content:
                        # 如果标题改变了，删除旧的，添加新的
                        if edited_title != selected_note:
                            del st.session_state.user_config["旅行笔记"][selected_note]
                        st.session_state.user_config["旅行笔记"][
                            edited_title
                        ] = edited_content
                        save_user_data()
                        st.rerun()
                    else:
                        st.warning("请填写标题和内容")

            with col2:
                if st.button("🗑️ 删除笔记"):
                    del st.session_state.user_config["旅行笔记"][selected_note]
                    save_user_data()
                    st.rerun()

    # 添加新笔记
    st.subheader("➕ 添加新笔记")
    new_note_title = st.text_input("笔记标题", key="new_note_title")
    new_note_content = st.text_area("笔记内容", height=200, key="new_note_content")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 添加笔记"):
            if new_note_title and new_note_content:
                st.session_state.user_config["旅行笔记"][
                    new_note_title
                ] = new_note_content
                save_user_data()
                st.rerun()
            else:
                st.warning("请填写标题和内容")


def edit_personal_info(role: Role):
    """编辑个人信息"""
    st.title("👤 编辑个人信息")

    current_info = st.session_state.user_config.get("个人笔记", "")

    st.subheader("✏️ 编辑个人笔记")
    edited_info = st.text_area(
        "个人信息内容", value=current_info, height=400, key="personal_info_content"
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("💾 保存"):
            st.session_state.user_config["个人笔记"] = edited_info
            save_user_data()

    with col2:
        if st.button("👁️ 预览"):
            st.session_state.preview_personal_info = True

    # 预览功能
    if st.session_state.get("preview_personal_info", False):
        st.subheader("👁️ 预览效果")
        st.markdown(edited_info, unsafe_allow_html=True)
        if st.button("❌ 关闭预览"):
            st.session_state.preview_personal_info = False
            st.rerun()


def userPage(user_config: OrderedDict) -> None:
    # Sidebar navigation
    # 包含: 基本信息, 属性, 熟练, 种族, 背景, 职业, 物品, 武器, 法术, 冒险故事, 旅行笔记, 个人信息
    # 其中: 冒险故事, 旅行笔记, 个人信息可以编辑
    # side bar 永远可见
    st.sidebar.image(LOGO_IMAGE_PATH, use_container_width=True)
    st.sidebar.title("角色信息")

    # 初始化当前选中的部分
    if "current_section" not in st.session_state:
        st.session_state.current_section = "基本信息"

    # 初始化编辑模式状态
    if "edit_mode" not in st.session_state:
        st.session_state.edit_mode = False

    role = Role(user_config)
    sections = [
        "基本信息",
        "属性",
        "熟练",
        "种族",
        "背景",
        "职业",
        "物品",
        "武器",
        "法术",
        "冒险故事",
        "旅行笔记",
        "个人信息",
    ]

    # 创建侧边栏按钮，当点击时更新当前选中的部分
    for section in sections:
        if st.sidebar.button(section, key=f"btn_{section}"):
            st.session_state.current_section = section
            st.session_state.edit_mode = False  # 切换部分时退出编辑模式
            pass
        pass

    # 添加登出按钮
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 登出"):
        # 清除用户会话状态
        keys_to_remove = [
            "user_config",
            "user_json_file",
            "group_name",
            "current_section",
            "edit_mode",
        ]
        for key in keys_to_remove:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    # 主页面内容
    current_section = st.session_state.current_section

    # 如果是可编辑的部分，显示编辑/查看切换按钮
    if current_section in EDITABLE_SECTIONS:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.title(f"📋")
        with col2:
            if st.session_state.edit_mode:
                if st.button("👁️ 查看模式"):
                    st.session_state.edit_mode = False
                    st.rerun()
            else:
                if st.button("✏️ 编辑模式"):
                    st.session_state.edit_mode = True
                    st.rerun()
    else:
        st.title(f"📋")

    # 显示内容
    if current_section in EDITABLE_SECTIONS and st.session_state.edit_mode:
        # 编辑模式
        if current_section == "旅行笔记":
            edit_notes(role)
        elif current_section == "个人信息":
            edit_personal_info(role)
    else:
        # 查看模式
        if current_section in FUNCTION_DICT:
            content = FUNCTION_DICT[current_section](role)
            st.markdown(content, unsafe_allow_html=True)
        else:
            st.error("未知的部分，请联系管理员。")

    pass


def main() -> None:
    # 如果用户已经登录，直接显示用户页面
    if "user_config" in st.session_state:
        userPage(st.session_state.user_config)
        return

    user_config: OrderedDict = loginPage()
    if user_config:
        # 保存用户配置到会话状态
        st.session_state.user_config = user_config
        # 重新运行以显示用户页面
        st.rerun()
        pass
    pass


if __name__ == "__main__":
    main()
    pass
