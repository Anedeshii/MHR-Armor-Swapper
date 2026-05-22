import os
import re
import shutil
import zipfile
import tempfile

import customtkinter as ctk

from tkinter import filedialog
from tkinter import messagebox


# =====================================================
# LOAD ARMOR DATABASE
# =====================================================

ARMORS = {}


def load_armor_database():

    global ARMORS

    ARMORS = {}

    db_path = "armor_database.txt"

    if not os.path.exists(db_path):
        print("================================")
        print("DATABASE NOT FOUND: armor_database.txt")
        print("Place armor_database.txt in the same folder as this app.")
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

                armor_id = model_name[2:]  # remove "pl"

                if not re.fullmatch(r'\d{3}', armor_id):
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
        self.geometry("950x780")
        self.minsize(800, 650)

        self.zip_path = None
        self.detected_id = None
        self.selected_armor = None

        self.create_ui()

    # =====================================================
    # UI
    # =====================================================

    def create_ui(self):

        # =====================================================
        # HEADER
        # =====================================================

        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(20, 0))

        title = ctk.CTkLabel(
            header_frame,
            text="Monster Hunter Rise Armor Swapper",
            font=("Arial", 30, "bold")
        )
        title.pack()

        subtitle = ctk.CTkLabel(
            header_frame,
            text="Professional Mod Converter",
            font=("Arial", 15),
            text_color="gray"
        )
        subtitle.pack(pady=(2, 0))

        # =====================================================
        # SELECT ZIP
        # =====================================================

        zip_frame = ctk.CTkFrame(self, corner_radius=12)
        zip_frame.pack(fill="x", padx=30, pady=20)

        ctk.CTkLabel(
            zip_frame,
            text="Step 1 — Select Mod ZIP",
            font=("Arial", 16, "bold")
        ).pack(pady=(15, 8))

        self.select_btn = ctk.CTkButton(
            zip_frame,
            text="📂  Select ZIP Mod",
            width=250,
            height=42,
            font=("Arial", 14, "bold"),
            command=self.select_zip
        )
        self.select_btn.pack(pady=5)

        self.file_label = ctk.CTkLabel(
            zip_frame,
            text="No ZIP selected",
            wraplength=800,
            text_color="gray",
            font=("Arial", 12)
        )
        self.file_label.pack(pady=(5, 8))

        # =====================================================
        # DETECTED ARMOR
        # =====================================================

        detect_frame = ctk.CTkFrame(self, corner_radius=12)
        detect_frame.pack(fill="x", padx=30, pady=(0, 10))

        ctk.CTkLabel(
            detect_frame,
            text="Detected Armor (from ZIP)",
            font=("Arial", 16, "bold")
        ).pack(pady=(15, 5))

        self.detect_label = ctk.CTkLabel(
            detect_frame,
            text="Waiting for ZIP...",
            font=("Arial", 22),
            text_color="#3a9eca"
        )
        self.detect_label.pack(pady=(0, 15))

        # =====================================================
        # ARMOR SELECTOR
        # =====================================================

        self.main_frame = ctk.CTkFrame(self, corner_radius=12)
        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 10)
        )

        ctk.CTkLabel(
            self.main_frame,
            text="Step 2 — Select Target Armor",
            font=("Arial", 16, "bold")
        ).pack(pady=(15, 5))

        # Search entry
        self.search_entry = ctk.CTkEntry(
            self.main_frame,
            width=500,
            height=38,
            placeholder_text="🔍  Type to search armor...",
            font=("Arial", 13)
        )
        self.search_entry.pack(pady=(5, 10))
        self.search_entry.bind("<KeyRelease>", self.filter_armors)

        # Scrollable list
        self.scroll_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            width=700,
            height=260
        )
        self.scroll_frame.pack(pady=5, padx=10)

        # Build armor list
        self.armor_names = sorted([
            f"{name}  ({aid})"
            for aid, name in ARMORS.items()
        ])

        self.load_armor_buttons(self.armor_names)

        # Selected armor display
        self.selected_label = ctk.CTkLabel(
            self.main_frame,
            text="No armor selected",
            font=("Arial", 15),
            text_color="gray"
        )
        self.selected_label.pack(pady=(10, 5))

        # =====================================================
        # CONVERT BUTTON + STATUS
        # =====================================================

        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=30, pady=(0, 15))

        self.convert_btn = ctk.CTkButton(
            bottom_frame,
            text="⚙️  Convert Mod",
            width=320,
            height=55,
            font=("Arial", 18, "bold"),
            fg_color="#1f6aa5",
            hover_color="#144870",
            command=self.convert_mod,
            state="disabled"
        )
        self.convert_btn.pack(pady=(10, 5))

        self.status = ctk.CTkLabel(
            bottom_frame,
            text="✅  Ready — Select a ZIP to begin",
            font=("Arial", 13),
            text_color="green"
        )
        self.status.pack(pady=(0, 5))

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
                width=650,
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
            btn.pack(pady=2, padx=5, fill="x")

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

        filtered = [
            armor for armor in self.armor_names
            if query in armor.lower()
        ]

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

        filename = os.path.basename(path)
        self.file_label.configure(
            text=f"📦  {filename}",
            text_color="white"
        )

        self.set_status("🔍  Detecting armor from ZIP...", "yellow")
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

            temp_dir = tempfile.mkdtemp()
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

        # 1. Replace ID inside text-readable files
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

        # 2. Rename files containing old_id
        for root, dirs, files in os.walk(root_dir, topdown=False):
            for file in files:
                if old_id in file:
                    old_path = os.path.join(root, file)
                    new_path = os.path.join(root, file.replace(old_id, new_id))
                    try:
                        os.rename(old_path, new_path)
                    except Exception as e:
                        print(f"Rename file error: {e}")

        # 3. Rename folders containing old_id
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
                    path = os.path.join(root, file)
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
