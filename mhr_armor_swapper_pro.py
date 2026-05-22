import os
import re
import shutil
import zipfile
import tempfile

import customtkinter as ctk

from tkinter import filedialog
from tkinter import messagebox


# ==========================================
# LOAD ARMOR DATABASE
# ==========================================

ARMORS = {}

def load_armor_database():

    try:

        with open(
            "armor_database.txt",
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            lines = f.readlines()

        for line in lines:

            if "pl" not in line:
                continue

            # FIXED TAB SPLIT
            parts = line.strip().split("\t")

            if len(parts) < 7:
                continue

            try:

                armor_name = parts[1].strip()
                model_name = parts[5].strip()
                is_valid = parts[-1].strip()

                if not model_name.startswith("pl"):
                    continue

                if is_valid != "True":
                    continue

                if armor_name == "":
                    continue

                if "#Rejected#" in armor_name:
                    continue

                armor_id = model_name.replace("pl", "")

                if armor_id not in ARMORS:
                    ARMORS[armor_id] = armor_name

            except:
                pass

        print(f"Loaded {len(ARMORS)} armors.")
        print("TOTAL ARMORS:", len(ARMORS))

    except Exception as e:

        print("Failed loading database:", e)

load_armor_database()


# ==========================================
# UI SETTINGS
# ==========================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ==========================================
# MAIN APP
# ==========================================

class ArmorSwapper(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Monster Hunter Rise Armor Swapper")
        self.geometry("900x650")
        self.resizable(False, False)

        self.zip_path = None
        self.detected_id = None

        self.create_ui()

    # ==========================================
    # UI
    # ==========================================

    def create_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Monster Hunter Rise Armor Swapper",
            font=("Arial", 30, "bold")
        )

        title.pack(pady=20)

        subtitle = ctk.CTkLabel(
            self,
            text="Professional Mod Converter",
            font=("Arial", 16)
        )

        subtitle.pack()

        self.select_btn = ctk.CTkButton(
            self,
            text="Select ZIP Mod",
            width=250,
            height=45,
            command=self.select_zip
        )

        self.select_btn.pack(pady=30)

        self.file_label = ctk.CTkLabel(
            self,
            text="No ZIP selected",
            wraplength=700
        )

        self.file_label.pack()

        info_frame = ctk.CTkFrame(self)

        info_frame.pack(
            fill="x",
            padx=30,
            pady=30
        )

        detect_title = ctk.CTkLabel(
            info_frame,
            text="Detected Armor",
            font=("Arial", 18, "bold")
        )

        detect_title.pack(pady=(20, 10))

        self.detect_label = ctk.CTkLabel(
            info_frame,
            text="Waiting for ZIP...",
            font=("Arial", 24)
        )

        self.detect_label.pack(pady=(0, 20))

        replace_title = ctk.CTkLabel(
            info_frame,
            text="Replace With",
            font=("Arial", 18, "bold")
        )

        replace_title.pack()

        armor_names = sorted([
            f"{name} ({aid})"
            for aid, name in ARMORS.items()
        ])

        self.combo = ctk.CTkComboBox(
            info_frame,
            values=armor_names,
            width=400,
            height=40
        )

        self.combo.pack(pady=20)

        if armor_names:
            self.combo.set(armor_names[0])

        self.convert_btn = ctk.CTkButton(
            self,
            text="Convert Mod",
            width=300,
            height=55,
            font=("Arial", 18, "bold"),
            command=self.convert_mod
        )

        self.convert_btn.pack(pady=20)

        self.status = ctk.CTkLabel(
            self,
            text="Ready",
            font=("Arial", 14)
        )

        self.status.pack(pady=10)

    # ==========================================
    # SELECT ZIP
    # ==========================================

    def select_zip(self):

        path = filedialog.askopenfilename(
            filetypes=[("ZIP Files", "*.zip")]
        )

        if not path:
            return

        self.zip_path = path

        self.file_label.configure(text=path)

        detected = self.detect_armor(path)

        if detected:

            self.detected_id = detected

            armor_name = ARMORS.get(
                detected,
                "Unknown Armor"
            )

            self.detect_label.configure(
                text=f"{armor_name} ({detected})"
            )

        else:

            self.detect_label.configure(
                text="Armor Not Detected"
            )

    # ==========================================
    # DETECT ARMOR
    # ==========================================

    def detect_armor(self, zip_path):

        try:

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:

                names = zip_ref.namelist()

                print("========== ZIP CONTENT ==========")

                for n in names:
                    print(n)

                print("=================================")

                # PRIORITY 1
                # DETECT plXXX

                for name in names:

                    if "pl" in name.lower():

                        match = re.search(
                            r'pl(\d{3})',
                            name,
                            re.IGNORECASE
                        )

                        if match:

                            armor_id = match.group(1)

                            print("Detected via plXXX:", armor_id)

                            return armor_id

                # PRIORITY 2
                # DETECT f_legXXX

                for name in names:

                    match = re.search(
                        r'f_leg(\d{3})',
                        name,
                        re.IGNORECASE
                    )

                    if match:

                        armor_id = match.group(1)

                        print("Detected via f_legXXX:", armor_id)

                        return armor_id

                # PRIORITY 3
                # ANY 3 DIGIT

                for name in names:

                    match = re.search(
                        r'(\d{3})',
                        name
                    )

                    if match:

                        armor_id = match.group(1)

                        print("Detected generic:", armor_id)

                        return armor_id

        except Exception as e:

            print("DETECTION ERROR:", e)

            return None

        return None

    # ==========================================
    # CONVERT MOD
    # ==========================================

    def convert_mod(self):

        if not self.zip_path:

            messagebox.showerror(
                "Error",
                "Please select ZIP mod first"
            )

            return

        if not self.detected_id:

            messagebox.showerror(
                "Error",
                "Could not detect armor"
            )

            return

        selected = self.combo.get()

        match = re.search(
            r'\((\d{3})\)',
            selected
        )

        if not match:

            messagebox.showerror(
                "Error",
                "Please select target armor"
            )

            return

        new_id = match.group(1)

        old_id = self.detected_id

        try:

            self.status.configure(
                text="Extracting ZIP..."
            )

            self.update()

            temp_dir = tempfile.mkdtemp()

            extract_dir = os.path.join(
                temp_dir,
                "extract"
            )

            with zipfile.ZipFile(
                self.zip_path,
                'r'
            ) as zip_ref:

                zip_ref.extractall(extract_dir)

            self.status.configure(
                text="Replacing armor IDs..."
            )

            self.update()

            self.replace_all(
                extract_dir,
                old_id,
                new_id
            )

            output_path = filedialog.asksaveasfilename(
                defaultextension=".zip",
                initialfile=f"converted_{new_id}.zip",
                filetypes=[("ZIP", "*.zip")]
            )

            if not output_path:
                return

            self.status.configure(
                text="Creating ZIP..."
            )

            self.update()

            self.create_zip(
                extract_dir,
                output_path
            )

            shutil.rmtree(temp_dir)

            self.status.configure(
                text="Done!"
            )

            messagebox.showinfo(
                "Success",
                f"Converted successfully!\n\nSaved:\n{output_path}"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

            self.status.configure(
                text="Failed"
            )

    # ==========================================
    # REPLACE ALL
    # ==========================================

    def replace_all(
        self,
        root_dir,
        old_id,
        new_id
    ):

        # REPLACE CONTENT

        for root, dirs, files in os.walk(root_dir):

            for file in files:

                file_path = os.path.join(
                    root,
                    file
                )

                try:

                    with open(
                        file_path,
                        'r',
                        encoding='utf-8'
                    ) as f:

                        content = f.read()

                    content = content.replace(
                        old_id,
                        new_id
                    )

                    with open(
                        file_path,
                        'w',
                        encoding='utf-8'
                    ) as f:

                        f.write(content)

                except:
                    pass

        # RENAME FILES

        for root, dirs, files in os.walk(
            root_dir,
            topdown=False
        ):

            for file in files:

                if old_id in file:

                    old_path = os.path.join(
                        root,
                        file
                    )

                    new_file = file.replace(
                        old_id,
                        new_id
                    )

                    new_path = os.path.join(
                        root,
                        new_file
                    )

                    os.rename(
                        old_path,
                        new_path
                    )

        # RENAME FOLDERS

        for root, dirs, files in os.walk(
            root_dir,
            topdown=False
        ):

            for d in dirs:

                if old_id in d:

                    old_path = os.path.join(
                        root,
                        d
                    )

                    new_dir = d.replace(
                        old_id,
                        new_id
                    )

                    new_path = os.path.join(
                        root,
                        new_dir
                    )

                    os.rename(
                        old_path,
                        new_path
                    )

    # ==========================================
    # CREATE ZIP
    # ==========================================

    def create_zip(
        self,
        folder,
        output
    ):

        with zipfile.ZipFile(
            output,
            'w',
            zipfile.ZIP_DEFLATED
        ) as zipf:

            for root, dirs, files in os.walk(folder):

                for file in files:

                    path = os.path.join(
                        root,
                        file
                    )

                    arcname = os.path.relpath(
                        path,
                        folder
                    )

                    zipf.write(
                        path,
                        arcname
                    )


# ==========================================
# RUN APP
# ==========================================

if __name__ == "__main__":

    app = ArmorSwapper()

    app.mainloop()

