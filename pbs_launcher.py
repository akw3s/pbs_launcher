import os
import subprocess
from pathlib import Path
import customtkinter as ctk

# --------------------
# THEME
# --------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# --------------------
# PATHS FOR DETECTION
# --------------------
PATHS = {
    "Roblox Studio": [
        Path(os.getenv("LOCALAPPDATA")) / "Roblox" / "Versions"
    ],
    "Godot Engine": [
        Path("C:/Program Files"),
        Path("C:/Program Files (x86)"),
        Path(os.getenv("USERPROFILE")) / "Desktop",
        Path(os.getenv("USERPROFILE")) / "Downloads"
    ],
    "Unity Hub": [
        Path("C:/Program Files/Unity Hub/Unity Hub.exe")
    ],
    "Unity Editor": [
        Path("C:/Program Files/Unity/Editor/Unity.exe"),
        Path("C:/Program Files (x86)/Unity/Editor/Unity.exe")
    ],
    "Blender": [
        Path("C:/Program Files/Blender Foundation/Blender"),
        Path("C:/Program Files")
    ],
    "VS Code": [
        Path("C:/Users") / os.getlogin() / "AppData/Local/Programs/Microsoft VS Code/Code.exe"
    ],
    "Unreal Engine": [
        Path("C:/Program Files/Epic Games")
    ],
}

# --------------------
# DETECTION FUNCTIONS
# --------------------
def find_roblox_studio():
    base = PATHS["Roblox Studio"][0]
    if base.exists():
        for folder in base.iterdir():
            exe = folder / "RobloxStudioBeta.exe"
            if exe.exists():
                return exe
    return None

def find_godot():
    for path in PATHS["Godot Engine"]:
        if not path.exists():
            continue
        for item in path.glob("**/godot*.exe"):
            return item
    return None

def find_blender():
    for path in PATHS["Blender"]:
        if not path.exists():
            continue
        for exe in path.glob("**/blender.exe"):
            return exe
    return None

def find_unreal():
    for base in PATHS["Unreal Engine"]:
        if not base.exists():
            continue
        for exe in base.glob("**/UE4Editor.exe"):
            return exe
        for exe in base.glob("**/UnrealEditor.exe"):
            return exe
    return None

def find_installed():
    found = {}

    if (r := find_roblox_studio()): found["Roblox Studio"] = r
    if (g := find_godot()): found["Godot Engine"] = g
    if PATHS["Unity Hub"][0].exists(): found["Unity Hub"] = PATHS["Unity Hub"][0]
    for p in PATHS["Unity Editor"]:
        if p.exists(): found["Unity Editor"] = p
    if (b := find_blender()): found["Blender"] = b
    if PATHS["VS Code"][0].exists(): found["VS Code"] = PATHS["VS Code"][0]
    if (u := find_unreal()): found["Unreal Engine"] = u

    return found

# --------------------
# LAUNCH FUNCTION
# --------------------
def launch(path):
    subprocess.Popen([str(path)])

# --------------------
# UI
# --------------------
app = ctk.CTk()
app.title("Purple Band Studios - Developer Launcher")
app.geometry("1920x1080")

# Title
title = ctk.CTkLabel(app, text="Purple Band Studios", font=("Segoe UI", 28, "bold"))
title.pack(pady=(20,5))

sub = ctk.CTkLabel(app, text="Developer Tools Launcher", font=("Segoe UI", 18))
sub.pack(pady=(0,20))

installed = find_installed()

if not installed:
    ctk.CTkLabel(app,
        text="No supported developer tools installed.",
        font=("Segoe UI", 16)).pack(pady=20)
else:
    container = ctk.CTkFrame(app)
    container.pack(fill="both", expand=True, padx=60, pady=20)

    left_frame = ctk.CTkFrame(container)
    left_frame.pack(side="left", anchor="n", expand=True)

    right_frame = ctk.CTkFrame(container)
    right_frame.pack(side="right", anchor="n", expand=True)

    items = list(installed.items())
    mid = (len(items) + 1) // 2
    left_items = items[:mid]
    right_items = items[mid:]

    def make_button(parent, name, exe):
        btn = ctk.CTkButton(
            parent,
            text=name,
            width=400,
            height=70,
            corner_radius=15,
            font=("Segoe UI", 18, "bold"),
            fg_color="#914EFF",
            hover_color="#6D30DB",
            command=lambda p=exe: launch(p)
        )
        btn.pack(pady=(10,6))
        sep = ctk.CTkFrame(parent, width=400, height=2, fg_color="#2B2B2B")
        sep.pack(pady=(0,10))

    for name, exe in left_items:
        make_button(left_frame, name, exe)

    for name, exe in right_items:
        make_button(right_frame, name, exe)

app.mainloop()
