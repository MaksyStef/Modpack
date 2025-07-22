import os
import tkinter as tk
from tkinter import ttk, simpledialog

# Custom colors
BG_COLOR = "#080705"
FG_COLOR = "#EEE5E9"
BTN_BG = "#1a1a1a"
BTN_HOVER = "#333333"
FONT = ("Segoe UI", 14)

FOLDER_ICON = "📁"
FILE_ICON = "📄"

class DirectoryTreeDialog(simpledialog.Dialog):
    def __init__(self, parent, base_path, prechecked=None):
        self.base_path = os.path.abspath(base_path)
        self.prechecked = set(os.path.abspath(p) for p in (prechecked or []))
        self.checked_paths = set()
        super().__init__(parent, title="Select Files and Folders")

    def body(self, master):
        self.master.configure(bg=BG_COLOR)
        self.configure(bg=BG_COLOR)

        # Prepare checkbox images
        self.img_unchecked = self.create_checkbox_image(checked=False)
        self.img_checked = self.create_checkbox_image(checked=True)

        # Container
        container = tk.Frame(master, bg=BG_COLOR)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview with modern styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background=BG_COLOR,
                        fieldbackground=BG_COLOR,
                        foreground=FG_COLOR,
                        font=FONT,
                        borderwidth=0,
                        rowheight=30)
        style.configure("Vertical.TScrollbar",
                        gripcount=0,
                        background=BG_COLOR,
                        troughcolor=BG_COLOR,
                        bordercolor=BG_COLOR,
                        arrowcolor=FG_COLOR,
                        width=8)
        style.map("Vertical.TScrollbar",
                  background=[("active", "#222222"), ("!active", BG_COLOR)])

        self.tree = ttk.Treeview(container, columns=("fullpath",), show="tree", selectmode="none")
        self.tree.pack(side="left", fill="both", expand=True)

        vsb = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview, style="Vertical.TScrollbar")
        vsb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=vsb.set)

        # Populate root
        self._insert_items("", self.base_path)
        self.tree.bind("<<TreeviewOpen>>", self.on_open)
        self.tree.bind("<Button-1>", self.on_click)

        return container  # initial focus

    def create_checkbox_image(self, checked=False):
        img = tk.PhotoImage(width=16, height=16)
        img.put(("white",), to=(0, 0, 15, 15))
        img.put(("black",), to=(0, 0, 15, 0))
        img.put(("black",), to=(0, 0, 0, 15))
        img.put(("black",), to=(15, 0, 15, 15))
        img.put(("black",), to=(0, 15, 15, 15))

        if checked:
            # ✓ Checkmark centered
            for i in range(5, 10):
                img.put(("black",), to=(i, 15 - i, i + 1, 16 - i))
            for i in range(8, 11):
                img.put(("black",), to=(i, i - 6, i + 1, i - 5))
        return img

    def _insert_items(self, parent, path):
        try:
            entries = sorted(os.listdir(path))
        except PermissionError:
            return

        for name in entries:
            full_path = os.path.join(path, name)
            is_dir = os.path.isdir(full_path)
            icon = FOLDER_ICON if is_dir else FILE_ICON
            is_checked = full_path in self.prechecked

            item_id = self.tree.insert(
                parent, "end",
                text=f"{icon}  {name}",
                image=self.img_checked if is_checked else self.img_unchecked,
                values=(full_path,)
            )

            if is_checked:
                self.checked_paths.add(full_path)

            if is_dir:
                self.tree.insert(item_id, "end")  # Dummy child

    def on_open(self, event):
        item_id = self.tree.focus()
        children = self.tree.get_children(item_id)
        if len(children) == 1 and not self.tree.item(children[0], "values"):
            self.tree.delete(children[0])
            full_path = self.tree.item(item_id, "values")[0]
            self._insert_items(item_id, full_path)

    def on_click(self, event):
        item_id = self.tree.identify_row(event.y)
        region = self.tree.identify("element", event.x, event.y)
        if item_id and region == "image":
            self._toggle_item(item_id)

    def _toggle_item(self, item_id):
        full_path = self.tree.item(item_id, "values")[0]
        if full_path in self.checked_paths:
            self.checked_paths.remove(full_path)
            self.tree.item(item_id, image=self.img_unchecked)
        else:
            self.checked_paths.add(full_path)
            self.tree.item(item_id, image=self.img_checked)

    def buttonbox(self):
        # Override default button box
        box = tk.Frame(self, bg=BG_COLOR)
        box.pack(side="bottom", fill="x", padx=10, pady=(0, 10))

        def style_btn(btn):
            btn.configure(
                bg=BTN_BG, fg=FG_COLOR,
                font=FONT,
                activebackground=BTN_HOVER,
                activeforeground=FG_COLOR,
                relief="flat",
                bd=0,
                padx=20,
                pady=8
            )
            btn.bind("<Enter>", lambda e: btn.configure(bg=BTN_HOVER))
            btn.bind("<Leave>", lambda e: btn.configure(bg=BTN_BG))

        ok_btn = tk.Button(box, text="OK", width=10, command=self.ok)
        cancel_btn = tk.Button(box, text="Cancel", width=10, command=self.cancel)

        style_btn(ok_btn)
        style_btn(cancel_btn)

        ok_btn.pack(side="right", padx=(5, 0))
        cancel_btn.pack(side="right", padx=(0, 5))

    def apply(self):
        self.result = list(self.checked_paths)


def ask_directory_tree_with_checkboxes(base_path, prechecked=None):
    root = tk.Tk()
    root.withdraw()
    dialog = DirectoryTreeDialog(root, base_path, prechecked)
    root.destroy()
    return dialog.result or []
