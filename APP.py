import json
import os
from datetime import datetime
import tkinter.colorchooser as colorchooser
import customtkinter as ctk

# 設定外觀模式與顏色主題
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

DATA_FILE = "tasks.json"
TAGS_FILE = "tags.json"

class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("工作待辦清單")
        self.geometry("850x750")
        self.minsize(780, 680)

        # 載入資料與標籤設定
        self.common_tags = self.load_tags()
        self.current_tag = ""
        self.current_color = list(self.common_tags.values())[0] if self.common_tags else "#f5d0d6"
        
        self.tasks = self.load_data()

        # 拖曳狀態變數
        self.drag_data = {"index": None, "widgets": []}

        # 建立 UI
        self.create_widgets()
        self.refresh_task_list()

    def load_tags(self):
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
            "紅豆泥": "#f5d0d6"
        }

    def save_tags(self):
        with open(TAGS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.common_tags, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data:
                        if "completed" not in item:
                            item["completed"] = False
                        if "created_date" not in item:
                            item["created_date"] = datetime.now().strftime("%Y-%m-%d")
                        if "completed_date" not in item:
                            item["completed_date"] = ""
                    return data
            except Exception:
                return []
        today = datetime.now().strftime("%Y-%m-%d")
        return [
            {"text": "新版DM", "tag": "紅豆泥", "color": "#f5d0d6", "completed": False, "created_date": today, "completed_date": ""},
            {"text": "電子版菜單製作", "tag": "", "color": "#f5d0d6", "completed": False, "created_date": today, "completed_date": ""},
            {"text": "pop文宣 中秋商品", "tag": "紅豆泥", "color": "#f5d0d6", "completed": False, "created_date": today, "completed_date": ""},
            {"text": "鹽埕a2圖片", "tag": "紅豆泥", "color": "#f5d0d6", "completed": False, "created_date": today, "completed_date": ""},
        ]

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=4)

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self, fg_color="#f8f9fa", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 標題列
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        title_label = ctk.CTkLabel(
            header_frame, text="📋 工作待辦清單", font=("Microsoft JhengHei", 20, "bold"), text_color="#333333"
        )
        title_label.pack(side="left")

        self.history_btn = ctk.CTkButton(
            header_frame, text="查看歷史完成 (0)", 
            fg_color="#e9ecef", text_color="#495057", hover_color="#dee2e6",
            font=("Microsoft JhengHei", 12), width=140, height=32,
            command=self.open_history_window
        )
        self.history_btn.pack(side="right")

        # 捲動任務清單區
        self.canvas_frame = ctk.CTkScrollableFrame(main_frame, fg_color="transparent", height=340)
        self.canvas_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # 下方新增任務控制面板
        input_panel = ctk.CTkFrame(main_frame, fg_color="#ffffff", corner_radius=12, border_width=1, border_color="#d0d7de")
        input_panel.pack(fill="x", padx=20, pady=(10, 20))

        top_input_row = ctk.CTkFrame(input_panel, fg_color="transparent")
        top_input_row.pack(fill="x", padx=15, pady=15)

        self.task_entry = ctk.CTkEntry(
            top_input_row, placeholder_text="輸入新工作內容...", 
            font=("Microsoft JhengHei", 14), height=40, fg_color="#ffffff", border_color="#ced4da"
        )
        self.task_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.tag_display_btn = ctk.CTkButton(
            top_input_row, text="分組標籤", fg_color="#f1f3f5", text_color="#6c757d",
            font=("Microsoft JhengHei", 13), width=100, height=40, state="disabled"
        )
        self.tag_display_btn.pack(side="left", padx=(0, 10))

        add_btn = ctk.CTkButton(
            top_input_row, text="新增工作", fg_color="#8e9bc2", hover_color="#7786b0", text_color="#ffffff",
            font=("Microsoft JhengHei", 14, "bold"), width=100, height=40,
            command=self.add_task
        )
        add_btn.pack(side="left")

        tag_row = ctk.CTkFrame(input_panel, fg_color="transparent")
        tag_row.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkLabel(tag_row, text="常用標籤：", font=("Microsoft JhengHei", 12), text_color="#6c757d").pack(side="left", padx=(0, 5))
        
        self.tags_container = ctk.CTkFrame(tag_row, fg_color="transparent")
        self.tags_container.pack(side="left", fill="x", expand=True)

        add_tag_btn = ctk.CTkButton(
            tag_row, text="標籤管理", fg_color="#e9ecef", text_color="#495057",
            hover_color="#dee2e6", font=("Microsoft JhengHei", 11), width=85, height=26,
            command=self.open_tag_manager_dialog
        )
        add_tag_btn.pack(side="right", padx=(5, 0))

        self.render_tag_buttons()

    def render_tag_buttons(self):
        for widget in self.tags_container.winfo_children():
            widget.destroy()

        for tag, tag_color in self.common_tags.items():
            is_selected = (self.current_tag == tag)
            btn_color = "#7786b0" if is_selected else tag_color
            text_color = "#ffffff" if is_selected else "#212529"
            
            t_btn = ctk.CTkButton(
                self.tags_container, text=tag, fg_color=btn_color, text_color=text_color,
                hover_color="#cbd5e1" if not is_selected else "#627099",
                font=("Microsoft JhengHei", 12), width=65, height=26,
                command=lambda t=tag: self.select_tag(t)
            )
            t_btn.pack(side="left", padx=3)
            t_btn.bind("<Button-3>", lambda e, t=tag: self.delete_tag(t))

    def select_tag(self, tag):
        if self.current_tag == tag:
            self.current_tag = ""
            self.tag_display_btn.configure(text="分組標籤", text_color="#6c757d")
        else:
            self.current_tag = tag
            if tag in self.common_tags:
                self.current_color = self.common_tags[tag]
            self.tag_display_btn.configure(text=tag, text_color="#111827")
        self.render_tag_buttons()

    def open_tag_manager_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("標籤管理")
        dialog.geometry("380x350")
        dialog.resizable(False, False)
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="➕ 新增分組標籤", font=("Microsoft JhengHei", 14, "bold")).pack(padx=20, pady=(15, 5), anchor="w")
        
        add_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        add_frame.pack(padx=20, pady=(0, 10), fill="x")

        name_entry = ctk.CTkEntry(add_frame, placeholder_text="輸入新標籤名稱...", width=240, font=("Microsoft JhengHei", 12))
        name_entry.pack(side="left", padx=(0, 10))

        selected_col = ctk.StringVar(value="#f5d0d6")

        def pick_custom_color():
            color_result = colorchooser.askcolor(title="選擇標籤及背景顏色")
            if color_result[1]:
                selected_col.set(color_result[1])
                col_btn.configure(fg_color=color_result[1])

        col_btn = ctk.CTkButton(
            add_frame, text="選色", fg_color="#f5d0d6", text_color="#212529",
            hover_color="#ced4da", font=("Microsoft JhengHei", 11), width=60, height=28,
            command=pick_custom_color
        )
        col_btn.pack(side="left")

        def save_new_tag():
            t_name = name_entry.get().strip()
            if t_name:
                chosen_color = selected_col.get()
                self.common_tags[t_name] = chosen_color
                self.save_tags()
                self.current_color = chosen_color
                self.render_tag_buttons()
                dialog.destroy()

        save_btn = ctk.CTkButton(dialog, text="確認新增標籤", fg_color="#8e9bc2", hover_color="#7786b0", command=save_new_tag, width=330, height=32)
        save_btn.pack(pady=(0, 15))

        ctk.CTkFrame(dialog, height=2, fg_color="#dee2e6").pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(dialog, text="🗑️ 刪除現有標籤 (點擊刪除)", font=("Microsoft JhengHei", 14, "bold")).pack(padx=20, pady=(10, 5), anchor="w")

        tag_scroll = ctk.CTkScrollableFrame(dialog, fg_color="transparent", height=130)
        tag_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        def refresh_tag_list_in_dialog():
            for widget in tag_scroll.winfo_children():
                widget.destroy()

            for t_name, t_col in self.common_tags.items():
                row = ctk.CTkFrame(tag_scroll, fg_color="transparent")
                row.pack(fill="x", pady=3)

                badge = ctk.CTkLabel(row, text=t_name, fg_color=t_col, text_color="#212529", corner_radius=4, width=80, height=26, font=("Microsoft JhengHei", 12))
                badge.pack(side="left", padx=(0, 10))

                def remove_this_tag(tn=t_name):
                    self.delete_tag(tn)
                    refresh_tag_list_in_dialog()

                del_btn = ctk.CTkButton(row, text="刪除", fg_color="#c25c4a", hover_color="#a84939", width=60, height=26, font=("Microsoft JhengHei", 11), command=remove_this_tag)
                del_btn.pack(side="right")

        refresh_tag_list_in_dialog()

    def delete_tag(self, tag):
        if tag in self.common_tags:
            del self.common_tags[tag]
            self.save_tags()
            if tag == self.current_tag:
                self.current_tag = ""
                self.tag_display_btn.configure(text="分組標籤", text_color="#6c757d")
            for task in self.tasks:
                if task["tag"] == tag:
                    task["tag"] = ""
            self.save_data()
            self.render_tag_buttons()
            self.refresh_task_list()

    def add_task(self):
        text = self.task_entry.get().strip()
        if not text:
            return
        
        today = datetime.now().strftime("%Y-%m-%d")
        new_task = {
            "text": text,
            "tag": self.current_tag,
            "color": self.current_color,
            "completed": False,
            "created_date": today,
            "completed_date": ""
        }
        self.tasks.append(new_task)
        self.save_data()
        
        self.task_entry.delete(0, "end")
        self.refresh_task_list()

    def toggle_task_status(self, original_index):
        today = datetime.now().strftime("%Y-%m-%d")
        self.tasks[original_index]["completed"] = True
        self.tasks[original_index]["completed_date"] = today
        self.save_data()
        self.refresh_task_list()

    def delete_task(self, original_index):
        del self.tasks[original_index]
        self.save_data()
        self.refresh_task_list()

    def edit_task(self, original_index):
        task = self.tasks[original_index]
        dialog = ctk.CTkToplevel(self)
        dialog.title("編輯工作項目")
        dialog.geometry("360x260")
        dialog.resizable(False, False)
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="修改工作內容：", font=("Microsoft JhengHei", 13)).pack(padx=20, pady=(20, 5), anchor="w")
        text_entry = ctk.CTkEntry(dialog, width=320, font=("Microsoft JhengHei", 13))
        text_entry.pack(padx=20, pady=(0, 10))
        text_entry.insert(0, task["text"])

        ctk.CTkLabel(dialog, text="選擇標籤：", font=("Microsoft JhengHei", 13)).pack(padx=20, pady=(0, 5), anchor="w")
        
        tag_var = ctk.StringVar(value=task["tag"])
        tag_combo = ctk.CTkComboBox(dialog, values=[""] + list(self.common_tags.keys()), variable=tag_var, width=320)
        tag_combo.pack(padx=20, pady=(0, 15))

        def save_edit():
            new_text = text_entry.get().strip()
            if new_text:
                task["text"] = new_text
                chosen_tag = tag_var.get()
                task["tag"] = chosen_tag
                if chosen_tag in self.common_tags:
                    task["color"] = self.common_tags[chosen_tag]
                self.save_data()
                self.refresh_task_list()
                dialog.destroy()

        save_btn = ctk.CTkButton(dialog, text="儲存修改", fg_color="#8e9bc2", hover_color="#7786b0", command=save_edit, width=120)
        save_btn.pack(pady=(0, 15))

    def open_history_window(self):
        history_win = ctk.CTkToplevel(self)
        history_win.title("歷史完成工作紀錄")
        history_win.geometry("620x450")
        history_win.minsize(550, 400)
        history_win.grab_set()

        ctk.CTkLabel(
            history_win, text="🏆 已完成的工作清單", font=("Microsoft JhengHei", 16, "bold"), text_color="#333333"
        ).pack(padx=20, pady=(20, 10), anchor="w")

        history_scroll = ctk.CTkScrollableFrame(history_win, fg_color="transparent")
        history_scroll.pack(fill="both", expand=True, padx=20, pady=10)

        def refresh_history_content():
            for widget in history_scroll.winfo_children():
                widget.destroy()

            completed_tasks = [(i, t) for i, t in enumerate(self.tasks) if t["completed"]]

            if not completed_tasks:
                ctk.CTkLabel(
                    history_scroll, text="目前沒有已完成的工作紀錄", font=("Microsoft JhengHei", 13), text_color="#adb5bd"
                ).pack(pady=40)
                return

            for orig_idx, task in completed_tasks:
                # 歷史區卡片也改成操場型 (corner_radius=22)
                card = ctk.CTkFrame(history_scroll, fg_color=task["color"], corner_radius=22, height=48)
                card.pack(fill="x", pady=4)
                card.pack_propagate(False)

                left_inner = ctk.CTkFrame(card, fg_color="transparent")
                left_inner.pack(side="left", padx=15, fill="y")

                if task["tag"]:
                    tag_badge = ctk.CTkLabel(
                        left_inner, text=task["tag"], fg_color="#ffffff", text_color="#495057",
                        corner_radius=10, font=("Microsoft JhengHei", 11), width=45, height=20
                    )
                    tag_badge.pack(side="left", padx=(0, 8))

                text_label = ctk.CTkLabel(
                    left_inner, text=task["text"], font=("Microsoft JhengHei", 13), text_color="#495057"
                )
                text_label.pack(side="left", padx=(0, 10))

                date_str = f"完成: {task.get('completed_date', 'N/A')}"
                date_label = ctk.CTkLabel(
                    left_inner, text=date_str, font=("Microsoft JhengHei", 11), text_color="#6c757d"
                )
                date_label.pack(side="left")

                right_inner = ctk.CTkFrame(card, fg_color="transparent")
                right_inner.pack(side="right", padx=15, fill="y")

                restore_btn = ctk.CTkButton(
                    right_inner, text="還原", fg_color="#3b82f6", hover_color="#2563eb",
                    font=("Microsoft JhengHei", 11, "bold"), width=50, height=26, corner_radius=13,
                    command=lambda idx=orig_idx: [
                        self.tasks[idx].update({"completed": False, "completed_date": ""}),
                        self.save_data(),
                        self.refresh_task_list(),
                        refresh_history_content()
                    ]
                )
                restore_btn.pack(side="left", padx=4)

                del_btn = ctk.CTkButton(
                    right_inner, text="刪除", fg_color="#c25c4a", hover_color="#a84939",
                    font=("Microsoft JhengHei", 11, "bold"), width=50, height=26, corner_radius=13,
                    command=lambda idx=orig_idx: [
                        self.delete_task(idx),
                        refresh_history_content()
                    ]
                )
                del_btn.pack(side="left")

        refresh_history_content()

    # ==================== 流暢自由拖曳排序核心事件 ====================
    def on_drag_start(self, event, uncompleted_idx):
        self.drag_data["index"] = uncompleted_idx

    def on_drag_motion(self, event):
        if self.drag_data["index"] is None:
            return
        
        uncompleted_indices = [i for i, t in enumerate(self.tasks) if not t["completed"]]
        if not uncompleted_indices:
            return

        current_vis_idx = self.drag_data["index"]
        
        target_vis_idx = current_vis_idx
        for idx, widget_info in enumerate(self.drag_data["widgets"]):
            widget = widget_info["widget"]
            y1 = widget.winfo_rooty()
            y2 = y1 + widget.winfo_height()
            if y1 <= event.y_root <= y2:
                target_vis_idx = idx
                break

        if target_vis_idx != current_vis_idx:
            real_current_idx = uncompleted_indices[current_vis_idx]
            real_target_idx = uncompleted_indices[target_vis_idx]
            
            self.tasks[real_current_idx], self.tasks[real_target_idx] = self.tasks[real_target_idx], self.tasks[real_current_idx]
            self.drag_data["index"] = target_vis_idx
            self.refresh_task_list()

    def on_drag_release(self, event):
        if self.drag_data["index"] is not None:
            self.drag_data["index"] = None
            self.save_data()
            self.refresh_task_list()
    # ============================================================

    def refresh_task_list(self):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        self.drag_data["widgets"] = []

        completed_count = sum(1 for t in self.tasks if t["completed"])
        self.history_btn.configure(text=f"查看歷史完成 ({completed_count})")

        uncompleted_tasks = [(i, t) for i, t in enumerate(self.tasks) if not t["completed"]]

        for vis_idx, (real_idx, task) in enumerate(uncompleted_tasks):
            # 將卡片的 corner_radius 設為 25（高度為 50），讓左右兩側呈現完美半圓形的操場膠囊外型
            card = ctk.CTkFrame(self.canvas_frame, fg_color=task["color"], corner_radius=18, height=50)
            card.pack(fill="x", pady=6)
            card.pack_propagate(False)

            self.drag_data["widgets"].append({"widget": card, "real_index": real_idx})

            left_inner = ctk.CTkFrame(card, fg_color="transparent")
            left_inner.pack(side="left", padx=15, fill="y")

            grip_label = ctk.CTkLabel(
                left_inner, text="≡", font=("Microsoft JhengHei", 18, "bold"), text_color="#6c757d", cursor="fleur"
            )
            grip_label.pack(side="left", padx=(0, 10))

            grip_label.bind("<Button-1>", lambda e, v_idx=vis_idx: self.on_drag_start(e, v_idx))
            grip_label.bind("<B1-Motion>", self.on_drag_motion)
            grip_label.bind("<ButtonRelease-1>", self.on_drag_release)

            if task["tag"]:
                tag_badge = ctk.CTkLabel(
                    left_inner, text=task["tag"], fg_color="#ffffff", text_color="#495057",
                    corner_radius=10, font=("Microsoft JhengHei", 11), width=50, height=22
                )
                tag_badge.pack(side="left", padx=(0, 10))

            text_label = ctk.CTkLabel(
                left_inner, text=task["text"], font=("Microsoft JhengHei", 14), text_color="#212529"
            )
            text_label.pack(side="left", padx=(0, 10))

            created_str = f"建立: {task.get('created_date', 'N/A')}"
            created_label = ctk.CTkLabel(
                left_inner, text=created_str, font=("Microsoft JhengHei", 11), text_color="#6c757d"
            )
            created_label.pack(side="left")

            right_inner = ctk.CTkFrame(card, fg_color="transparent")
            right_inner.pack(side="right", padx=15, fill="y")

            complete_btn = ctk.CTkButton(
                right_inner, text="完成", fg_color="#c1dced", hover_color="#a6cce7", text_color="#212529",
                font=("Microsoft JhengHei", 12, "bold"), width=55, height=28, corner_radius=14,
                command=lambda idx=real_idx: self.toggle_task_status(idx)
            )
            complete_btn.pack(side="left", padx=4)

            edit_btn = ctk.CTkButton(
                right_inner, text="編輯", fg_color="#868e96", hover_color="#495057",
                font=("Microsoft JhengHei", 12, "bold"), width=50, height=28, corner_radius=14,
                command=lambda idx=real_idx: self.edit_task(idx)
            )
            edit_btn.pack(side="left", padx=4)

            delete_btn = ctk.CTkButton(
                right_inner, text="刪除", fg_color="#c25c4a", hover_color="#a84939",
                font=("Microsoft JhengHei", 12, "bold"), width=50, height=28, corner_radius=14,
                command=lambda idx=real_idx: self.delete_task(idx)
            )
            delete_btn.pack(side="left")

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
