import platform
from importlib import resources
import os
from PIL import Image
from customtkinter import CTkImage


# ...............................  general gui stuff  ..................................
def configure_the_icon(root):
    """Configure the icon - in macos it changes the dock icon, in windows it changes
    all windows titlebar icons (taskbar cannot be changed without converting to exe)
    """
    if platform.system().startswith("Darwin"):
        try:
            from Cocoa import NSApplication, NSImage
        except ImportError:
            print("Unable to import pyobjc modules")
        else:
            with resources.path("autogaita.resources", "icon.icns") as icon_path:
                ns_application = NSApplication.sharedApplication()
                logo_ns_image = NSImage.alloc().initWithContentsOfFile_(str(icon_path))
                ns_application.setApplicationIconImage_(logo_ns_image)
    elif platform.system().startswith("win"):
        with resources.path("autogaita.resources", "icon.ico") as icon_path:
            root.iconbitmap(str(icon_path))


def fix_window_after_its_creation(window):
    """Perform some quality of life things after creating a window (root or Toplevel)"""
    window.attributes("-topmost", True)
    window.focus_set()
    window.after(100, lambda: window.attributes("-topmost", False))  # 100 ms


def maximise_widgets(window):
    """Maximises all widgets to look good in fullscreen"""
    # fix the grid to fill the window
    num_rows = window.grid_size()[1]  # maximise rows
    for r in range(num_rows):
        window.grid_rowconfigure(r, weight=1)
    num_cols = window.grid_size()[0]  # maximise cols
    for c in range(num_cols):
        window.grid_columnconfigure(c, weight=1)


# ..............................  change widget states  ................................


def change_widget_state_based_on_checkbox(cfg, key_to_check, widget_to_change):
    """Change the state of a widget based on state of another widget."""
    if cfg[key_to_check].get() is True:
        widget_to_change.configure(state="normal")
    elif cfg[key_to_check].get() is False:
        widget_to_change.configure(state="disabled")

def create_folder_icon():
    folder_icon_path = os.path.join(os.path.dirname(__file__), "folder.png")
    folder_icon_pil = Image.open(folder_icon_path)
    return CTkImage(
        light_image=folder_icon_pil,
        dark_image=folder_icon_pil,
        size=(20, 20)
    )
