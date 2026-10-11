import json
import os
from datetime import datetime
import pandas as pd
import streamlit as st

# 設定頁面標題與佈局
st.set_page_config(
    page_title="工作待辦清單", page_icon="📋", layout="centered"
)

# 資料儲存檔案路徑
DATA_FILE = "todo_data.json"


# 初始化載入與儲存資料
def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # 預設初始資料與版面一致
    return {
        "tags": {
            "紅斗泥": "#E0A9A9",
            "拍攝": "#D0E1D4",
            "修圖": "#D4E1E9",
            "會議": "#E9E1D4",
            "設計": "#E1D4E9",
        },
        "tasks": [
            {
                "title": "新版DM",
                "tag": "紅斗泥",
                "status": "pending",
                "created_at": "2026-10-10 00:33",
            },
            {
                "title": "電子版菜單製作",
                "tag": "紅斗泥",
                "status": "pending",
                "created_at": "2026-10-10 00:33",
            },
            {
                "title": "pop文宣 中秋商品",
                "tag": "紅斗泥",
                "status": "pending",
                "created_at": "2026-10-10 00:33",
            },
            {
                "title": "鹽埕a2圖片",
                "tag": "紅斗泥",
                "status": "pending",
                "created_at": "2026-10-10 00:33",
            },
        ],
    }


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if "app_data" not in st.session_state:
    st.session_state.app_data = load_data()

data = st.session_state.app_data

if "show_history" not in st.session_state:
    st.session_state.show_history = False

# 自訂 CSS 打造精緻圓角卡片與現代感外框
st.markdown(
    """
    <style>
    .main {
        background-color: #f7f8fa;
    }
    .stButton>button {
        border-radius: 6px;
        font-weight: 500;
        font-size: 13px;
        padding: 4px 10px;
        width: 100%;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==================== 頂部標題與切換按鈕 ====================
header_col1, header_col2 = st.columns([0.6, 0.4])
with header_col1:
    st.markdown("### 📋 工作待辦清單", unsafe_allow_html=True)
with header_col2:
    completed_count = len(
        [t for t in data["tasks"] if t.get("status") == "completed"]
    )
    history_btn_text = (
        "返回待辦清單"
        if st.session_state.show_history
        else f"查看歷史完成 ({completed_count})"
    )
    if st.button(history_btn_text, use_container_width=True):
        st.session_state.show_history = not st.session_state.show_history
        st.rerun()

st.markdown("<div style='margin-bottom: 10px;'></div>", unsafe_allow_html=True)

# ==================== 歷史完成頁面 ====================
if st.session_state.show_history:
    st.subheader("📜 歷史完成清單")
    completed_tasks = [
        t for t in data["tasks"] if t.get("status") == "completed"
    ]

    if not completed_tasks:
        st.info("目前尚無已完成的歷史紀錄。")
    else:
        for task in completed_tasks:
            orig_idx = data["tasks"].index(task)
            tag_color = data["tags"].get(task["tag"], "#E0A9A9")
            st.markdown(
                f"""
                <div style="background-color: #f1f3f5; border-left: 6px solid {tag_color}; padding: 12px 16px; border-radius: 8px; margin-bottom: 10px;">
                    <span style="text-decoration: line-through; color: #555; font-weight: 500; font-size: 16px;">{task['title']}</span><br>
                    <small style='color:gray;'>創建: {task['created_at']} | 完成: {task.get('completed_at', 'N/A')} &nbsp;|&nbsp; <span style="background-color:{tag_color}; color:#333; padding:1px 6px; border-radius:8px; font-size:11px;">{task["tag"]}</span></small>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("刪除此歷史紀錄", key=f"del_hist_{orig_idx}"):
                data["tasks"].pop(orig_idx)
                save_data(data)
                st.rerun()
    st.stop()

# ==================== 上半部：進行中的代辦清單 ====================
pending_tasks = [
    t for t in data["tasks"] if t.get("status", "pending") == "pending"
]

if not pending_tasks:
    st.info("目前沒有進行中的待辦事項，請在下方新增一個吧！")
else:
    for task in pending_tasks:
        orig_idx = data["tasks"].index(task)
        tag_color = data["tags"].get(task["tag"], "#E0A9A9")

        with st.container():
            st.markdown(
                f"""
                <div style="background-color: {tag_color}; padding: 10px 16px; border-radius: 8px; margin-bottom: 10px; display: flex; align-items: center;">
                """,
                unsafe_allow_html=True,
            )

            c_content, c_done, c_del = st.columns([0.76, 0.12, 0.12])

            with c_content:
                st.markdown(
                    f"""
                    <div style="display: flex; align-items: center; gap: 10px; padding-top: 4px;">
                        <span style="color: #444; font-size: 18px; cursor: grab;">≡</span>
                        <span style="background-color: rgba(255,255,255,0.7); color: #333; padding: 2px 8px; border-radius: 6px; font-size: 11px; font-weight: bold; white-space: nowrap;">{task["tag"]}</span>
                        <span style="font-size: 15px; font-weight: 500; color: #111;">{task['title']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with c_done:
                if st.button("完成", key=f"done_{orig_idx}"):
                    data["tasks"][orig_idx]["status"] = "completed"
                    data["tasks"][orig_idx]["completed_at"] = datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    )
                    save_data(data)
                    st.rerun()

            with c_del:
                if st.button("刪除", key=f"del_{orig_idx}"):
                    data["tasks"].pop(orig_idx)
                    save_data(data)
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

# ==================== 下半部：精美輸入區與標籤管理框 ====================
st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
st.markdown("---")

with st.container():
    st.markdown(
        """
        <div style="background-color: white; border: 1px solid #e0e0e0; padding: 20px; border-radius: 10px; box-shadow: 0 1px 4px rgba(0,0,0,0.02);">
        """,
        unsafe_allow_html=True,
    )

    col_input, col_select, col_btn = st.columns([0.5, 0.3, 0.2])

    with col_input:
        input_task_title = st.text_input(
            "輸入新工作內容...",
            key="input_task_title_box",
            label_visibility="collapsed",
            placeholder="輸入新工作內容...",
        )

    with col_select:
        tag_options = list(data["tags"].keys())
        selected_tag = st.selectbox(
            "分組標籤",
            tag_options,
            key="select_tag_box",
            label_visibility="collapsed",
        )

    with col_btn:
        if st.button("新增工作", use_container_width=True):
            if input_task_title.strip() == "":
                st.warning("請輸入工作內容！")
            else:
                new_task = {
                    "title": input_task_title,
                    "tag": selected_tag,
                    "status": "pending",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "completed_at": "",
                }
                data["tasks"].append(new_task)
                save_data(data)
                st.success("新增成功！")
                st.rerun()

    # 常用標籤列
    st.markdown(
        "<div style='font-size: 13px; color: #555; margin-top: 15px; margin-bottom: 8px;'>常用標籤：</div>",
        unsafe_allow_html=True,
    )
    tag_cols = st.columns(len(data["tags"]))
    for i, (t_name, t_color) in enumerate(data["tags"].items()):
        with tag_cols[i]:
            if st.button(
                f"{t_name} ✕", key=f"quick_del_tag_{t_name}", use_container_width=True
            ):
                if len(data["tags"]) > 1:
                    del data["tags"][t_name]
                    save_data(data)
                    st.rerun()
                else:
                    st.warning("至少保留一個標籤")

    # 顏色預覽與自訂顏色設定
    st.markdown(
        "<hr style='margin: 15px 0; border: none; border-top: 1px solid #eee;'>",
        unsafe_allow_html=True,
    )
    c_color_label, c_color_picker, c_custom_label, c_custom_picker = st.columns(
        [0.15, 0.35, 0.15, 0.35]
    )

    with c_color_label:
        st.markdown(
            "<div style='padding-top: 5px; font-size: 13px; color: #555;'>常用色：</div>",
            unsafe_allow_html=True,
        )
    with c_color_picker:
        curr_color = data["tags"].get(selected_tag, "#E0A9A9")
        st.markdown(
            f'<div style="width: 30px; height: 30px; background-color: {curr_color}; border-radius: 50%; border: 1px solid #ccc; display: inline-block;"></div>',
            unsafe_allow_html=True,
        )

    with c_custom_label:
        st.markdown(
            "<div style='padding-top: 5px; font-size: 13px; color: #555;'>自訂色：</div>",
            unsafe_allow_html=True,
        )
    with c_custom_picker:
        with st.popover("＋常用色 / 新增標籤", use_container_width=True):
            new_t_name = st.text_input("新標籤名稱", placeholder="例如：行政")
            new_t_color = st.color_picker("選擇顏色", "#E0A9A9")
            if st.button("確認新增"):
                if new_t_name.strip():
                    if new_t_name in data["tags"]:
                        st.warning("標籤已存在！")
                    else:
                        data["tags"][new_t_name] = new_t_color
                        save_data(data)
                        st.success("新增標籤成功！")
                        st.rerun()
                else:
                    st.warning("請輸入標籤名稱！")

    st.markdown("</div>", unsafe_allow_html=True)
