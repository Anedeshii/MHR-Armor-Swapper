import os
import re
import sys
import shutil
import zipfile
import tempfile

import customtkinter as ctk

from tkinter import filedialog
from tkinter import messagebox

def resource_path(relative_path):

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(
        base_path,
        relative_path
    )
# =====================================================
# LOAD ARMOR DATABASE
# =====================================================

ARMORS = {}

def load_armor_database():

    global ARMORS

    ARMORS = {}

    db_path = resource_path(
        "armor_database.txt"
    )

    if not os.path.exists(db_path):

        print("================================")
        print("DATABASE NOT FOUND")
        print(db_path)
        print("================================")

        return

    try:

        with open(
            db_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            lines = f.readlines()

        for line in lines:

            if "pl" not in line.lower():
                continue

            parts = line.strip().split("\t")

            if len(parts) < 6:
                continue

            try:

                armor_name = parts[1].strip()


                remove_words = [
                    "Helm",
                    "Mail",
                    "Coil",
                    "Greaves",
                    "Braces",
                    "Vambraces",
                    "Arms",
                    "Legs",
                    "Waist",
                    "Chest"
                ]

                for word in remove_words:

                    armor_name = re.sub(
                        rf'\b{word}\b',
                        '',
                        armor_name,
                        flags=re.IGNORECASE
                    )


                armor_name = re.sub(
                    r'\s+',
                    ' ',
                    armor_name
                ).strip()

                model_name = parts[5].strip()
                is_valid = parts[-1].strip()

                if not model_name.lower().startswith("pl"):
                    continue

                if is_valid != "True":
                    continue

                if not armor_name:
                    continue

                if "#Rejected#" in armor_name:
                    continue

                armor_id = model_name[2:]

                if not re.fullmatch(
                    r'\d{3}',
                    armor_id
                ):
                    continue

                if armor_id not in ARMORS:
                    ARMORS[armor_id] = armor_name

            except Exception:
                continue

        print("================================")
        print(f"TOTAL ARMORS LOADED: {len(ARMORS)}")
        print("================================")

    except Exception as e:

        print("DATABASE ERROR:", e)


load_armor_database()



# =====================================================
# UI SETTINGS
# =====================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# =====================================================
# MAIN APP
# =====================================================

class ArmorSwapper(ctk.CTk):

    def __init__(self):

        super().__init__()


        self.title("Monster Hunter Rise Armor Swapper")
        self.geometry("980x800")
        self.minsize(900, 750)

        self.zip_path      = None
        self.detected_id   = None
        self.selected_armor = None

        self.create_ui()

    # =====================================================
    # UI  —  layout: TOP fixed  |  MIDDLE scrollable  |  BOTTOM fixed
    # =====================================================

    def create_ui(self):

        # ── TOP SECTION (fixed, never scrolls away) ──────────────────
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=24, pady=(18, 6))

        # Title
        ctk.CTkLabel(
            top,
            text="Monster Hunter Rise Armor Swapper",
            font=("Arial", 28, "bold")
        ).pack()

        ctk.CTkLabel(
            top,
            text="Professional Mod Converter",
            font=("Arial", 14),
            text_color="gray"
        ).pack(pady=(2, 10))

        # Step 1 — ZIP
        zip_card = ctk.CTkFrame(top, corner_radius=12)
        zip_card.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            zip_card,
            text="Step 1 — Select Mod ZIP",
            font=("Arial", 15, "bold")
        ).pack(pady=(12, 6))

        self.select_btn = ctk.CTkButton(
            zip_card,
            text="📂  Select ZIP Mod",
            width=240,
            height=40,
            font=("Arial", 13, "bold"),
            command=self.select_zip
        )
        self.select_btn.pack(pady=4)

        self.file_label = ctk.CTkLabel(
            zip_card,
            text="No ZIP selected",
            wraplength=860,
            text_color="gray",
            font=("Arial", 12)
        )
        self.file_label.pack(pady=(2, 10))

        # Detected armor
        det_card = ctk.CTkFrame(top, corner_radius=12)
        det_card.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            det_card,
            text="Detected Armor (from ZIP)",
            font=("Arial", 15, "bold")
        ).pack(pady=(12, 4))

        self.detect_label = ctk.CTkLabel(
            det_card,
            text="Waiting for ZIP...",
            font=("Arial", 20),
            text_color="#3a9eca"
        )
        self.detect_label.pack(pady=(0, 12))

        # Step 2 header + search (fixed, stays visible)
        sel_header = ctk.CTkFrame(self, fg_color="transparent")
        sel_header.pack(fill="x", padx=24)

        ctk.CTkLabel(
            sel_header,
            text="Step 2 — Select Target Armor",
            font=("Arial", 15, "bold")
        ).pack(pady=(4, 4))

        self.search_entry = ctk.CTkEntry(
            sel_header,
            width=500,
            height=36,
            placeholder_text="🔍  Type to search armor...",
            font=("Arial", 13)
        )
        self.search_entry.pack(pady=(0, 6))
        self.search_entry.bind("<KeyRelease>", self.filter_armors)

        # ── MIDDLE SECTION (expands / scrolls) ───────────────────────
        list_frame = ctk.CTkFrame(self, fg_color="transparent")
        list_frame.pack(fill="both", expand=True, padx=24, pady=4)

        self.scroll_frame = ctk.CTkScrollableFrame(
            list_frame,
            corner_radius=10
        )
        self.scroll_frame.pack(fill="both", expand=True)

        # Build armor list
        self.armor_names = sorted([
            f"{name}  ({aid})"
            for aid, name in ARMORS.items()
        ])
        self.load_armor_buttons(self.armor_names)

        # ── BOTTOM SECTION (fixed, always visible) ───────────────────
        bottom = ctk.CTkFrame(self, corner_radius=12)
        bottom.pack(fill="x", padx=24, pady=(6, 14))

        self.selected_label = ctk.CTkLabel(
            bottom,
            text="No armor selected",
            font=("Arial", 14),
            text_color="gray"
        )
        self.selected_label.pack(pady=(12, 6))

        self.convert_btn = ctk.CTkButton(
            bottom,
            text="⚙️  Convert Mod",
            width=300,
            height=52,
            font=("Arial", 18, "bold"),
            fg_color="#1f6aa5",
            hover_color="#144870",
            command=self.convert_mod,
            state="disabled"
        )
        self.convert_btn.pack(pady=(0, 8))

        self.status = ctk.CTkLabel(
            bottom,
            text="✅  Ready — Select a ZIP to begin",
            font=("Arial", 12),
            text_color="#3ecf8e"
        )
        self.status.pack(pady=(0, 10))

    # =====================================================
    # LOAD ARMOR BUTTONS
    # =====================================================

    def load_armor_buttons(self, armor_list):

        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not armor_list:
            ctk.CTkLabel(
                self.scroll_frame,
                text="No armors found.",
                font=("Arial", 13),
                text_color="gray"
            ).pack(pady=20)
            return

        for armor in armor_list:

            btn = ctk.CTkButton(
                self.scroll_frame,
                text=armor,
                height=34,
                anchor="w",
                font=("Arial", 12),
                fg_color="transparent",
                border_width=1,
                border_color="gray30",
                text_color=("gray10", "gray90"),
                hover_color=("gray75", "gray25"),
                command=lambda a=armor: self.select_armor(a)
            )
            btn.pack(pady=2, padx=6, fill="x")

    # =====================================================
    # SELECT ARMOR
    # =====================================================

    def select_armor(self, armor):

        self.selected_armor = armor

        self.selected_label.configure(
            text=f"✔  Selected:  {armor}",
            text_color="#3ecf8e"
        )

        self.convert_btn.configure(state="normal")

    # =====================================================
    # FILTER ARMORS
    # =====================================================

    def filter_armors(self, event=None):

        query = self.search_entry.get().strip().lower()

        if not query:
            self.load_armor_buttons(self.armor_names)
            return

        filtered = [a for a in self.armor_names if query in a.lower()]
        self.load_armor_buttons(filtered)

    # =====================================================
    # SELECT ZIP
    # =====================================================

    def select_zip(self):

        path = filedialog.askopenfilename(
            title="Select Mod ZIP",
            filetypes=[("ZIP Files", "*.zip")]
        )

        if not path:
            return

        self.zip_path = path

        self.file_label.configure(
            text=f"📦  {os.path.basename(path)}",
            text_color="white"
        )

        self.set_status("🔍  Detecting armor...", "yellow")
        self.update()

        detected = self.detect_armor(path)

        if detected:

            self.detected_id = detected

            armor_name = ARMORS.get(detected, "Unknown Armor")

            self.detect_label.configure(
                text=f"{armor_name}  (ID: {detected})",
                text_color="#3a9eca"
            )

            self.set_status("✅  Armor detected. Now select target armor.", "green")

        else:

            self.detected_id = None

            self.detect_label.configure(
                text="⚠️  Armor Not Detected",
                text_color="orange"
            )

            self.set_status("⚠️  Could not detect armor ID from ZIP.", "orange")

    # =====================================================
    # DETECT ARMOR
    # =====================================================

    def detect_armor(self, zip_path):

        try:

            with zipfile.ZipFile(zip_path, 'r') as zf:

                names = zf.namelist()

                for name in names:
                    m = re.search(r'pl(\d{3})', name, re.IGNORECASE)
                    if m:
                        return m.group(1)

                for name in names:
                    m = re.search(r'f_leg(\d{3})', name, re.IGNORECASE)
                    if m:
                        return m.group(1)

        except Exception as e:
            print("DETECTION ERROR:", e)

        return None

    # =====================================================
    # CONVERT MOD
    # =====================================================

    def convert_mod(self):

        if not self.zip_path:
            messagebox.showerror("Error", "Please select a ZIP mod first.")
            return

        if not self.detected_id:
            messagebox.showerror("Error", "Could not detect armor ID from ZIP.")
            return

        if not self.selected_armor:
            messagebox.showerror("Error", "Please select a target armor.")
            return

        m = re.search(r'\((\d{3})\)', self.selected_armor)

        if not m:
            messagebox.showerror("Error", "Could not read target armor ID. Please re-select.")
            return

        new_id = m.group(1)
        old_id = self.detected_id

        if old_id == new_id:
            messagebox.showinfo("Info", "Source and target armor are the same. Nothing to convert.")
            return

        try:

            self.set_status("⏳  Extracting ZIP...", "yellow")
            self.update()

            temp_dir    = tempfile.mkdtemp()
            extract_dir = os.path.join(temp_dir, "extract")

            with zipfile.ZipFile(self.zip_path, 'r') as zf:
                zf.extractall(extract_dir)

            self.set_status(f"🔄  Replacing ID {old_id} → {new_id}...", "yellow")
            self.update()

            self.replace_all(extract_dir, old_id, new_id)

            output_path = filedialog.asksaveasfilename(
                title="Save Converted Mod",
                defaultextension=".zip",
                initialfile=f"converted_pl{new_id}.zip",
                filetypes=[("ZIP Files", "*.zip")]
            )

            if not output_path:
                shutil.rmtree(temp_dir)
                self.set_status("❌  Cancelled.", "orange")
                return

            self.set_status("📦  Creating output ZIP...", "yellow")
            self.update()

            self.create_zip(extract_dir, output_path)
            shutil.rmtree(temp_dir)

            self.set_status("✅  Done! Mod converted successfully.", "green")

            messagebox.showinfo(
                "Success",
                f"Mod converted successfully!\n\n"
                f"Source ID:  {old_id}\n"
                f"Target ID:  {new_id}\n\n"
                f"Saved to:\n{output_path}"
            )

        except Exception as e:

            print("CONVERT ERROR:", e)
            messagebox.showerror("Error", str(e))
            self.set_status("❌  Conversion failed.", "red")

    # =====================================================
    # REPLACE ALL
    # =====================================================

    def replace_all(self, root_dir, old_id, new_id):

        # 1. Replace content inside text-readable files
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    if old_id in content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content.replace(old_id, new_id))
                except Exception:
                    pass  # skip binary files

        # 2. Rename files
        for root, dirs, files in os.walk(root_dir, topdown=False):
            for file in files:
                if old_id in file:
                    old_path = os.path.join(root, file)
                    new_path = os.path.join(root, file.replace(old_id, new_id))
                    try:
                        os.rename(old_path, new_path)
                    except Exception as e:
                        print(f"Rename file error: {e}")

        # 3. Rename folders
        for root, dirs, files in os.walk(root_dir, topdown=False):
            for d in dirs:
                if old_id in d:
                    old_path = os.path.join(root, d)
                    new_path = os.path.join(root, d.replace(old_id, new_id))
                    try:
                        os.rename(old_path, new_path)
                    except Exception as e:
                        print(f"Rename dir error: {e}")

    # =====================================================
    # CREATE ZIP
    # =====================================================

    def create_zip(self, folder, output):

        with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder):
                for file in files:
                    path    = os.path.join(root, file)
                    arcname = os.path.relpath(path, folder)
                    zipf.write(path, arcname)

    # =====================================================
    # HELPER
    # =====================================================

    def set_status(self, text, color="white"):

        color_map = {
            "green":  "#3ecf8e",
            "yellow": "#f5c842",
            "orange": "#f5a623",
            "red":    "#f55050",
            "white":  "white",
        }

        self.status.configure(
            text=text,
            text_color=color_map.get(color, "white")
        )


# =====================================================
# RUN APP
# =====================================================

if __name__ == "__main__":

    app = ArmorSwapper()
    app.mainloop()
