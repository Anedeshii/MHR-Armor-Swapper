import os
import re
import sys
import shutil
import zipfile
import tempfile

import customtkinter as ctk

from tkinter import filedialog
from tkinter import messagebox

from armor_database import ARMOR_DATA


ARMORS = ARMOR_DATA


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class ArmorSwapper(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title(
            "Monster Hunter Rise Armor Swapper"
        )

        self.geometry("980x800")

        self.minsize(900, 750)

        self.configure(
            fg_color="#0f1117"
        )

        self.zip_path = None

        self.detected_id = None

        self.selected_armor = None

        self.create_ui()

    def clean_name(self, armor_name):

        remove_words = [
            "Helm", "Mail", "Coil", "Greaves",
            "Braces", "Vambraces", "Arms", "Legs",
            "Waist", "Chest", "Head", "Headgear",
            "Hat", "Hood", "Mask", "Crown",
            "Cap", "Hair-tie", "Vizor", "Face",
            "Boots", "Feet", "Foot", "Pants",
            "Leggings", "Gloves", "Belt", "Suit",
            "Torso", "Cloak", "Gaiters", "Guards",
            "Sleeves", "Pauldrons", "Breastplate",
            "Ribplate", "Cover", "Vest", "Jacket",
            "Robe", "Folia", "Roots", "Branch",
            "Branches", "Brachia", "Crura",
            "Thorax", "Elytra", "Tassets",
            "Obi", "Hakama", "Sash", "Glare",
            "Cista", "Grip", "Cocoon",
            "Crus", "Creeper", "Vertex",
            "Shinguards", "Gauntlets",
            "Armguards", "Scarf"
        ]

        for word in remove_words:

            armor_name = re.sub(
                rf"\b{word}\b",
                "",
                armor_name,
                flags=re.IGNORECASE
            )

        armor_name = re.sub(
            r"\s+",
            " ",
            armor_name
        ).strip()

        armor_name = armor_name.replace(
            "'s",
            ""
        )

        return armor_name

    def create_card(self, master):

        return ctk.CTkFrame(
            master,
            corner_radius=14,
            fg_color="#161b22",
            border_width=1,
            border_color="#30363d"
        )

    def create_ui(self):

        top = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        top.pack(
            fill="x",
            padx=24,
            pady=(18, 6)
        )

        ctk.CTkLabel(
            top,
            text="Monster Hunter Rise Armor Swapper",
            font=("Arial", 28, "bold"),
            text_color="#e6edf3"
        ).pack()

        ctk.CTkLabel(
            top,
            text="Professional Mod Converter",
            font=("Arial", 14),
            text_color="#8b949e"
        ).pack(
            pady=(2, 10)
        )

        zip_card = self.create_card(top)

        zip_card.pack(
            fill="x",
            pady=(0, 8)
        )

        ctk.CTkLabel(
            zip_card,
            text="Step 1 - Select Mod ZIP",
            font=("Arial", 15, "bold"),
            text_color="#e6edf3"
        ).pack(
            pady=(12, 6)
        )

        self.select_btn = ctk.CTkButton(
            zip_card,
            text="Select ZIP Mod",
            width=240,
            height=40,
            font=("Arial", 13, "bold"),
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.select_zip
        )

        self.select_btn.pack(
            pady=4
        )

        self.file_label = ctk.CTkLabel(
            zip_card,
            text="No ZIP selected",
            wraplength=860,
            text_color="#8b949e",
            font=("Arial", 12)
        )

        self.file_label.pack(
            pady=(2, 10)
        )

        det_card = self.create_card(top)

        det_card.pack(
            fill="x",
            pady=(0, 8)
        )

        ctk.CTkLabel(
            det_card,
            text="Detected Armor",
            font=("Arial", 15, "bold"),
            text_color="#e6edf3"
        ).pack(
            pady=(12, 4)
        )

        self.detect_label = ctk.CTkLabel(
            det_card,
            text="Waiting for ZIP...",
            font=("Arial", 20, "bold"),
            text_color="#38bdf8"
        )

        self.detect_label.pack(
            pady=(0, 12)
        )

        sel_header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        sel_header.pack(
            fill="x",
            padx=24
        )

        ctk.CTkLabel(
            sel_header,
            text="Step 2 - Select Target Armor",
            font=("Arial", 15, "bold"),
            text_color="#e6edf3"
        ).pack(
            pady=(4, 4)
        )

        self.search_entry = ctk.CTkEntry(
            sel_header,
            width=520,
            height=38,
            placeholder_text="Type to search armor...",
            font=("Arial", 13),
            fg_color="#0d1117",
            border_color="#30363d",
            text_color="#e6edf3",
            placeholder_text_color="#8b949e"
        )

        self.search_entry.pack(
            pady=(0, 6)
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.filter_armors
        )

        list_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        list_frame.pack(
            fill="both",
            expand=True,
            padx=24,
            pady=4
        )

        self.scroll_frame = ctk.CTkScrollableFrame(
            list_frame,
            corner_radius=12,
            fg_color="#161b22",
            border_width=1,
            border_color="#30363d"
        )

        self.scroll_frame.pack(
            fill="both",
            expand=True
        )

        self.armor_names = sorted([
            f"{self.clean_name(name)} ({aid})"
            for aid, name in ARMORS.items()
        ])

        self.load_armor_buttons(
            self.armor_names
        )

        bottom = self.create_card(self)

        bottom.pack(
            fill="x",
            padx=24,
            pady=(6, 14)
        )

        self.selected_label = ctk.CTkLabel(
            bottom,
            text="No armor selected",
            font=("Arial", 14),
            text_color="#8b949e"
        )

        self.selected_label.pack(
            pady=(12, 6)
        )

        self.convert_btn = ctk.CTkButton(
            bottom,
            text="Convert Mod",
            width=300,
            height=52,
            font=("Arial", 18, "bold"),
            fg_color="#22c55e",
            hover_color="#16a34a",
            command=self.convert_mod,
            state="disabled"
        )

        self.convert_btn.pack(
            pady=(0, 8)
        )

        self.status = ctk.CTkLabel(
            bottom,
            text="Ready - Select a ZIP to begin",
            font=("Arial", 12),
            text_color="#22c55e"
        )

        self.status.pack(
            pady=(0, 10)
        )

    def load_armor_buttons(self, armor_list):

        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not armor_list:

            ctk.CTkLabel(
                self.scroll_frame,
                text="No armors found.",
                font=("Arial", 13),
                text_color="#8b949e"
            ).pack(
                pady=20
            )

            return

        for armor in armor_list:

            btn = ctk.CTkButton(
                self.scroll_frame,
                text=armor,
                height=34,
                anchor="w",
                font=("Arial", 12),
                fg_color="#161b22",
                border_width=1,
                border_color="#30363d",
                text_color="#e6edf3",
                hover_color="#1f2937",
                command=lambda a=armor: self.select_armor(a)
            )

            btn.pack(
                pady=2,
                padx=6,
                fill="x"
            )

    def select_armor(self, armor):

        self.selected_armor = armor

        self.selected_label.configure(
            text=f"Selected: {armor}",
            text_color="#22c55e"
        )

        self.convert_btn.configure(
            state="normal"
        )

    def filter_armors(self, event=None):

        query = self.search_entry.get().strip().lower()

        if not query:

            self.load_armor_buttons(
                self.armor_names
            )

            return

        filtered = [
            a for a in self.armor_names
            if query in a.lower()
        ]

        self.load_armor_buttons(filtered)

    def select_zip(self):

        path = filedialog.askopenfilename(
            title="Select Mod ZIP",
            filetypes=[("ZIP Files", "*.zip")]
        )

        if not path:
            return

        self.zip_path = path

        self.file_label.configure(
            text=os.path.basename(path),
            text_color="#e6edf3"
        )

        self.set_status(
            "Detecting armor...",
            "yellow"
        )

        self.update()

        detected = self.detect_armor(path)

        if detected:

            self.detected_id = detected

            armor_name = ARMORS.get(
                detected,
                "Unknown Armor"
            )

            armor_name = self.clean_name(
                armor_name
            )

            self.detect_label.configure(
                text=f"{armor_name} (ID: {detected})",
                text_color="#38bdf8"
            )

            self.set_status(
                "Armor detected. Select target armor.",
                "green"
            )

        else:

            self.detected_id = None

            self.detect_label.configure(
                text="Armor Not Detected",
                text_color="#f97316"
            )

            self.set_status(
                "Could not detect armor ID.",
                "orange"
            )

    def detect_armor(self, zip_path):

        try:

            with zipfile.ZipFile(
                zip_path,
                "r"
            ) as zf:

                names = zf.namelist()

                for name in names:

                    m = re.search(
                        r"pl(\d{3})",
                        name,
                        re.IGNORECASE
                    )

                    if m:
                        return m.group(1)

                for name in names:

                    m = re.search(
                        r"f_leg(\d{3})",
                        name,
                        re.IGNORECASE
                    )

                    if m:
                        return m.group(1)

        except:
            pass

        return None

    def convert_mod(self):

        if not self.zip_path:

            messagebox.showerror(
                "Error",
                "Please select a ZIP mod first."
            )

            return

        if not self.detected_id:

            messagebox.showerror(
                "Error",
                "Could not detect armor ID."
            )

            return

        if not self.selected_armor:

            messagebox.showerror(
                "Error",
                "Please select target armor."
            )

            return

        m = re.search(
            r"\((\d{3})\)",
            self.selected_armor
        )

        if not m:

            messagebox.showerror(
                "Error",
                "Could not read target armor ID."
            )

            return

        old_id = self.detected_id

        new_id = m.group(1)

        if old_id == new_id:

            messagebox.showinfo(
                "Info",
                "Source and target armor are identical."
            )

            return

        temp_dir = None

        try:

            self.set_status(
                "Extracting ZIP...",
                "yellow"
            )

            self.update()

            temp_dir = tempfile.mkdtemp()

            extract_dir = os.path.join(
                temp_dir,
                "extract"
            )

            with zipfile.ZipFile(
                self.zip_path,
                "r"
            ) as zf:

                zf.extractall(extract_dir)

            self.set_status(
                f"Replacing ID {old_id} -> {new_id}...",
                "yellow"
            )

            self.update()

            self.replace_all(
                extract_dir,
                old_id,
                new_id
            )

            output_path = filedialog.asksaveasfilename(
                title="Save Converted Mod",
                defaultextension=".zip",
                initialfile=f"converted_pl{new_id}.zip",
                filetypes=[("ZIP Files", "*.zip")]
            )

            if not output_path:

                self.set_status(
                    "Cancelled.",
                    "orange"
                )

                return

            self.set_status(
                "Creating output ZIP...",
                "yellow"
            )

            self.update()

            self.create_zip(
                extract_dir,
                output_path
            )

            self.set_status(
                "Done! Mod converted successfully.",
                "green"
            )

            messagebox.showinfo(
                "Success",
                f"Mod converted successfully!\n\n"
                f"Source ID: {old_id}\n"
                f"Target ID: {new_id}\n\n"
                f"Saved to:\n{output_path}"
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e)
            )

            self.set_status(
                "Conversion failed.",
                "red"
            )

        finally:

            if temp_dir and os.path.exists(temp_dir):

                shutil.rmtree(temp_dir)

    def replace_all(self, root_dir, old_id, new_id):

        for root, dirs, files in os.walk(root_dir):

            for file in files:

                file_path = os.path.join(
                    root,
                    file
                )

                try:

                    with open(
                        file_path,
                        "r",
                        encoding="utf-8"
                    ) as f:

                        content = f.read()

                    if old_id in content:

                        with open(
                            file_path,
                            "w",
                            encoding="utf-8"
                        ) as f:

                            f.write(
                                content.replace(
                                    old_id,
                                    new_id
                                )
                            )

                except:
                    pass

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

                    new_path = os.path.join(
                        root,
                        file.replace(
                            old_id,
                            new_id
                        )
                    )

                    try:

                        os.rename(
                            old_path,
                            new_path
                        )

                    except:
                        pass

        for root, dirs, files in os.walk(
            root_dir,
            topdown=False
        ):

            for directory in dirs:

                if old_id in directory:

                    old_path = os.path.join(
                        root,
                        directory
                    )

                    new_path = os.path.join(
                        root,
                        directory.replace(
                            old_id,
                            new_id
                        )
                    )

                    try:

                        os.rename(
                            old_path,
                            new_path
                        )

                    except:
                        pass

    def create_zip(self, folder, output):

        with zipfile.ZipFile(
            output,
            "w",
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

    def set_status(self, text, color="white"):

        color_map = {
            "green": "#22c55e",
            "yellow": "#eab308",
            "orange": "#f97316",
            "red": "#ef4444",
            "white": "#e6edf3"
        }

        self.status.configure(
            text=text,
            text_color=color_map.get(
                color,
                "#e6edf3"
            )
        )


if __name__ == "__main__":

    app = ArmorSwapper()

    app.mainloop()