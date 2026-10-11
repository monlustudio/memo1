import json
import os
from datetime import datetime
import pandas as pd
import streamlit as st

# 設定頁面標題與佈局
st.set_page_config(
    page_title="工作待辦清單", page_icon="📋", layout="centered"
)

DATA_FILE = "tasks.json"
TAGS_FILE = "tags.json"


# 初始化載入與儲存資料
def load_tags():
    if os.path.exists(TAGS_FILE):
        try:
            with open(TAGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "拍攝": "#ffd8a8",
        "修圖": "#bac8ff",
        "會議": "#eebefa",
        "設計": "#c3fae8",
        "紅豆泥": "#f5d0d6",
    }


def save_tags(tags):
    with open(TAGS_FILE, "w", encoding="utf-8") as f:
        json.dump(tags, f, ensure_ascii=False, indent=4)


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    if "completed" not in item:
                        item["completed"] = False
                    if "created_date" not in item:
                        item["created_date"] = datetime.now().strftime(
                            "%Y-%m-%d"
                        )
                    if "completed_date" not in item:
                        item["completed_date"] = ""
                return data
        except Exception:
            return []
    today = datetime.now().strftime("%Y-%m-%d")
    return [
        {
            "text": "新版DM",
            "tag": "紅豆泥",
            "color": "#f5d0d6",
            "completed": False,
            "created_date": today,
            "completed_date": "",
        },
        {
            "text": "電子版菜單製作",
            "tag": "",
            "color": "#f5d0d6",
            "completed": False,
            "created_date": today,
            "completed_date": "",
        },
        {
            "text": "pop文宣 中秋商品",
            "tag": "紅豆泥",
            "color": "#f5d0d6",
            "completed": False,
            "created_date": today,
            "completed_date": "",
        },
        {
            "text": "鹽埕a2圖片",
            "tag": "紅豆泥",
            "color": "#f5d0d6",
            "completed": False,
            "created_date": today,
            "completed_date": "",
        },
    ]


def save_data(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)


if "tasks" not in st.session_state:
    st.session_state.tasks = load_data()
if "common_tags" not in st.session_state:
    st.session_state.common_tags = load_tags()
if "show_history" not in st.session_state:
    st.session_state.show_history = False
if "selected_tag" not in st.session_state:
    st.session_state.selected_tag = ""

# 自訂 CSS 打造圓角膠囊卡片與精緻介面
st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        border-radius: 14px;
        font-weight: 500;
        font-size: 13px;
        padding: 4px 12px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 標題與歷史完成切換按鈕
header_col1, header_col2 = st.columns([0.6, 0.4])
with header_col1:
    st.markdown("### 📋 工作待辦清單", unsafe_allow_html=True)
with header_col2:
    completed_count = sum(1 for t in st.session_state.tasks if t["completed"])
    btn_text = (
        "返回待辦清單"
        if st.session_state.show_history
        else f"查看歷史完成 ({completed_count})"
    )
    if st.button(btn_text, use_container_width=True):
        st.session_state.show_history = not st.session_state.show_history
        st.rerun()

st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

# 歷史完成頁面
if st.session_state.show_history:
    st.subheader("🏆 已完成的工作清單")
    completed_tasks = [
        (i, t) for i, t in enumerate(st.session_state.tasks) if t["completed"]
    ]

    if not completed_tasks:
        st.info("目前沒有已完成的工作紀錄")
    else:
        for orig_idx, task in completed_tasks:
            card_color = task.get("color", "#f5d0d6")
            st.markdown(
                f"""
                <div style="background-color: {card_color}; padding: 12px 18px; border-radius: 22px; margin-bottom: 8px; display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <span style="background-color: white; color: #495057; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: bold; margin-right: 8px;">{task["tag"]}</span>
                        <span style="text-decoration: line-through; color: #495057; font-weight: 500;">{task['text']}</span>
                        <span style="color: #6c757d; font-size: 11px; margin-left: 12px;">完成: {task.get('completed_date', 'N/A')}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            col_res, col_del = st.columns([0.5, 0.5])
            with col_res:
                if st.button("還原", key=f"restore_{orig_idx}"):
                    st.session_state.tasks[orig_idx]["completed"] = False
                    st.session_state.tasks[orig_idx]["completed_date"] = ""
                    save_data(st.session_state.tasks)
                    st.rerun()
            with col_del:
                if st.button("刪除", key=f"del_hist_{orig_idx}"):
                    st.session_state.tasks.pop(orig_idx)
                    save_data(st.session_state.tasks)
                    st.rerun()
    st.stop()

# 進行中的待辦清單
uncompleted_tasks = [
    (i, t) for i, t in enumerate(st.session_state.tasks) if not t["completed"]
]

if not uncompleted_tasks:
    st.info("目前沒有進行中的待辦事項，請在下方新增一個吧！")
else:
    for real_idx, task in uncompleted_tasks:
        card_color = task.get("color", "#f5d0d6")
        tag_text = task["tag"] if task["tag"] else "無標籤"

        with st.container():
            st.markdown(
                f"""
                <div style="background-color: {card_color}; padding: 10px 16px; border-radius: 18px; margin-bottom: 8px; display: flex; align-items: center;">
                """,
                unsafe_allow_html=True,
            )

            c_info, c_comp, c_edit, c_del = st.columns([0.64, 0.12, 0.12, 0.12])

            with c_info:
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: center; gap: 8px; padding-top: 4px;">
                        <span style="color: #6c757d; font-size: 16px;">≡</span>
                        <span style="background-color: white; color: #495057; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: bold;">{tag_text}</span>
                        <span style="font-size: 14px; font-weight: 500; color: #212529;">{task['text']}</span>
                        <span style="font-size: 11px; color: #6c757d;">建立: {task.get('created_date', 'N/A')}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with c_comp:
                if st.button("完成", key=f"comp_{real_idx}"):
                    today = datetime.now().strftime("%Y-%m-%d")
                    st.session_state.tasks[real_idx]["completed"] = True
                    st.session_state.tasks[real_idx]["completed_date"] = today
                    save_data(st.session_state.tasks)
                    st.rerun()

            with c_edit:
                with st.popover("編輯"):
                    new_text = st.text_input(
                        "修改內容",
                        value=task["text"],
                        key=f"edit_text_{real_idx}",
                    )
                    tag_list = [""] + list(st.session_state.common_tags.keys())
                    current_idx = (
                        tag_list.index(task["tag"])
                        if task["tag"] in tag_list
                        else 0
                    )
                    new_tag = st.selectbox(
                        "選擇標籤",
                        tag_list,
                        index=current_idx,
                        key=f"edit_tag_{real_idx}",
                    )

                    if st.button("儲存修改", key=f"save_edit_{real_idx}"):
                        st.session_state.tasks[real_idx]["text"] = new_text
                        st.session_state.tasks[real_idx]["tag"] = new_tag
                        if new_tag in st.session_state.common_tags:
                            st.session_state.tasks[real_idx]["color"] = (
                                st.session_state.common_tags[new_tag]
                            )
                        save_data(st.session_state.tasks)
                        st.success("修改成功！")
                        st.rerun()

            with c_del:
                if st.button("刪除", key=f"del_{real_idx}"):
                    st.session_state.tasks.pop(real_idx)
                    save_data(st.session_state.tasks)
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

# 下方控制面板：新增工作與標籤管理
st.markdown("<hr style='margin: 25px 0;'>", unsafe_allow_html=True)

with st.container():
    st.markdown(
        """
        <div style="background-color: #ffffff; border: 1px solid #d0d7de; padding: 20px; border-radius: 12px;">
        """,
        unsafe_allow_html=True,
    )

    col_in, col_tag_sel, col_add = st.columns([0.5, 0.3, 0.2])

    with col_in:
        new_task_text = st.text_input(
            "輸入新工作內容...",
            label_visibility="collapsed",
            placeholder="輸入新工作內容...",
            key="main_task_input",
        )

    with col_tag_sel:
        tag_options = ["(無標籤)"] + list(st.session_state.common_tags.keys())
        chosen_tag_disp = st.selectbox(
            "分組標籤",
            tag_options,
            label_visibility="collapsed",
            key="main_tag_select",
        )

    with col_add:
        if st.button("新增工作", use_container_width=True):
            if new_task_text.strip():
                actual_tag = (
                    "" if chosen_tag_disp == "(無標籤)" else chosen_tag_disp
                )
                actual_color = (
                    st.session_state.common_tags.get(actual_tag, "#f5d0d6")
                    if actual_tag
                    else "#f5d0d6"
                )
                today = datetime.now().strftime("%Y-%m-%d")

                new_task = {
                    "text": new_task_text.strip(),
                    "tag": actual_tag,
                    "color": actual_color,
                    "completed": False,
                    "created_date": today,
                    "completed_date": "",
                }
                st.session_state.tasks.append(new_task)
                save_data(st.session_state.tasks)
                st.rerun()

    # 常用標籤列與標籤管理彈窗
    st.markdown(
        "<div style='font-size: 13px; color: #6c757d; margin-top: 15px; margin-bottom: 8px;'>常用標籤：</div>",
        unsafe_allow_html=True,
    )
    tag_cols = st.columns(len(st.session_state.common_tags) + 1)
    for i, (t_name, t_col) in enumerate(st.session_state.common_tags.items()):
        with tag_cols[i]:
            if st.button(f"{t_name} ✕", key=f"quick_del_{t_name}", use_container_width=True):
                del st.session_state.common_tags[t_name]
                save_tags(st.session_state.common_tags)
                for t in st.session_state.tasks:
                    if t["tag"] == t_name:
                        t["tag"] = ""
                save_data(st.session_state.tasks)
                st.rerun()

    with tag_cols[-1]:
        with st.popover("＋ 標籤管理", use_container_width=True):
            st.markdown("**新增標籤**")
            new_t_name = st.text_input("新標籤名稱", placeholder="例如：行政")
            new_t_color = st.color_picker("標籤與背景顏色", "#f5d0d6")
            if st.button("確認新增"):
                if new_t_name.strip():
                    st.session_state.common_tags[new_t_name.strip()] = new_t_color
                    save_tags(st.session_state.common_tags)
                    st.success("新增標籤成功！")
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
