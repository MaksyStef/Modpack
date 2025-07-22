import os
import tkinter as tk
from tkinter import ttk, simpledialog
from PIL import Image, ImageTk # Requires Pillow: pip install Pillow

# Custom theme colors
BG_COLOR = "#080705"
FG_COLOR = "#EEE5E9"
BTN_BG = "#1a1a1a"
BTN_HOVER = "#333333"
FONT = ("Segoe UI", 12)

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

        # --- FIX 1 (Revisited): More Robust Feather Icon Removal ---
        # Method A: Try setting to an empty bitmap string (your original approach, should work)
        try:
            self.iconbitmap("")
        except tk.TclError:
            # This handles cases where "" might not be supported.
            # On some systems (especially Linux with specific window managers),
            # an explicit empty PhotoImage might be needed, or it might fall back
            # to a system default if no .ico is provided.
            # Method B: Create a tiny, transparent PNG as an icon using Pillow
            # This is more reliable cross-platform for truly blanking the icon.
            try:
                # Create a 1x1 transparent image
                img_transparent = Image.new('RGBA', (1, 1), (255, 255, 255, 0))
                # Convert to PhotoImage
                self.tk_transparent_icon = ImageTk.PhotoImage(img_transparent)
                # Set as window icon
                self.wm_iconphoto(True, self.tk_transparent_icon)
            except Exception as e:
                # Fallback if Pillow isn't installed or there's another issue
                # print(f"Warning: Could not set transparent icon: {e}")
                pass # Continue without setting a custom blank icon

        # Prepare checkbox images
        self.img_unchecked = self.create_checkbox_image(checked=False)
        self.img_checked = self.create_checkbox_image(checked=True)

        # === Treeview Frame ===
        # --- FIX 3 (Revisited - Part 1): Ensure container has no border/highlight ---
        # Added `highlightbackground` for even more robustness
        container = tk.Frame(master, bg=BG_COLOR, bd=0, highlightthickness=0, highlightbackground=BG_COLOR)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # === Treeview Styling ===
        style = ttk.Style()
        style.theme_use("clam")

        # Configure the main 'Treeview' element style
        style.configure("Treeview",
                        background=BG_COLOR,
                        fieldbackground=BG_COLOR,
                        foreground=FG_COLOR,
                        font=FONT,
                        # --- FIX 3 (Revisited - Part 2): Remove white border from Treeview via style ---
                        # `borderwidth` and `highlightthickness` are the primary controls.
                        # Setting `relief="flat"` is also crucial for some themes.
                        borderwidth=0,
                        highlightthickness=0,
                        relief="flat", # Explicitly set relief to flat
                        rowheight=30
                       )
        # --- FIX 3 (Revisited - Part 3): Remove focus outline by mapping colors ---
        # This maps the focus border color to the background color when the widget has focus.
        # This is often the most effective way to eliminate the "annoying outline".
        style.map("Treeview",
                  background=[("selected", BTN_HOVER), ("focus", BG_COLOR)], # Keeps selection color, sets focus to BG
                  foreground=[("selected", FG_COLOR), ("focus", FG_COLOR)],
                  # You might also need to map the 'bordercolor' if it's explicitly drawn on focus
                  bordercolor=[("focus", BG_COLOR)]
                 )


        style.configure("Treeview.Item",
                        padding=(5, 0, 0, 0)
                       )

        style.configure("Vertical.TScrollbar",
                        gripcount=0,
                        background=BG_COLOR,
                        troughcolor=BG_COLOR,
                        bordercolor=BG_COLOR,
                        arrowcolor=FG_COLOR,
                        width=8)
        style.map("Vertical.TScrollbar",
                  background=[("active", "#222222"), ("!active", BG_COLOR)])

        # --- Treeview Widget Creation ---
        # No borderwidth/highlightthickness here, as confirmed previously.
        self.tree = ttk.Treeview(container, columns=("fullpath",), show="tree", selectmode="none")
        self.tree.pack(side="left", fill="both", expand=True)

        # Create and link the vertical scrollbar to the Treeview
        vsb = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview, style="Vertical.TScrollbar")
        vsb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=vsb.set)

        self._insert_items("", self.base_path)

        # Bind events
        self.tree.bind("<<TreeviewOpen>>", self.on_open)
        self.tree.bind("<Button-1>", self.on_click)

        # --- FIX 3 (Revisited - Part 4): Remove widget-specific focus rings ---
        # For a ttk widget, the `takefocus` option can sometimes prevent a default outline.
        # However, the `style.map` is usually more effective for `ttk.Treeview`.
        # self.tree.configure(takefocus=False) # Uncomment if the above doesn't fully work

        return container

    def create_checkbox_image(self, checked=False):
        img = tk.PhotoImage(width=16, height=16)
        img.put(("white",), to=(0, 0, 15, 15))
        img.put(("black",), to=(0, 0, 15, 0))
        img.put(("black",), to=(0, 0, 0, 15))
        img.put(("black",), to=(15, 0, 15, 15))
        img.put(("black",), to=(0, 15, 15, 15))

        if checked:
            for i in range(4, 9):
                img.put(("black",), to=(i, i + 2, i + 1, i + 3))
            for i in range(8, 13):
                img.put(("black",), to=(i, 16 - i, i + 1, 17 - i))
        return img

    def _insert_items(self, parent, path):
        try:
            entries = sorted(os.listdir(path))
        except PermissionError:
            return

        for name in entries:
            full_path = os.path.join(path, name)
            is_dir = os.path.isdir(full_path)
            icon_char = FOLDER_ICON if is_dir else FILE_ICON

            is_checked = full_path in self.prechecked

            item_id = self.tree.insert(
                parent, "end",
                text=f"{icon_char}  {name}",
                image=self.img_checked if is_checked else self.img_unchecked,
                values=(full_path,)
            )

            if is_checked:
                self.checked_paths.add(full_path)

            if is_dir:
                self.tree.insert(item_id, "end")

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
        box = tk.Frame(self, bg=BG_COLOR)
        box.pack(side="bottom", fill="x", padx=10, pady=(0, 12))

        pad_left = tk.Frame(box, bg=BG_COLOR)
        pad_left.pack(side="left", expand=True)
        pad_right = tk.Frame(box, bg=BG_COLOR)
        pad_right.pack(side="right", expand=True)

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

        cancel_btn.pack(side="left", padx=10)
        ok_btn.pack(side="left", padx=10)

    def apply(self):
        self.result = list(self.checked_paths)

def ask_directory_tree_with_checkboxes(base_path, prechecked=None):
    root = tk.Tk()
    root.withdraw()
    dialog = DirectoryTreeDialog(root, base_path, prechecked)
    root.destroy()
    return dialog.result or []
