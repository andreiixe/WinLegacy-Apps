import os
import shutil
import win32com.client
import ctypes
import sys

INSTALL_DIR = os.path.join(os.getenv('APPDATA'), 'Spotify')
EXECUTABLE_NAME = 'Spotify.exe'
START_MENU_FOLDER = 'Spotify'
DESKTOP_SHORTCUT_NAME = 'Spotify.exe.lnk'

def is_admin():
    """Check if the script is running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Relaunch the script with administrator privileges."""
    script = sys.argv[0]
    params = " ".join(sys.argv[1:])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f"{script} {params}", None, 1)

def remove_start_menu_shortcut():
    shell = win32com.client.Dispatch("WScript.Shell")
    start_menu_path = shell.SpecialFolders("StartMenu")
    app_folder_path = os.path.join(start_menu_path, START_MENU_FOLDER)

    # Remove the Start Menu folder if it exists
    if os.path.exists(app_folder_path):
        shutil.rmtree(app_folder_path)
        print(f"Removed Start Menu folder: {app_folder_path}")
    else:
        print("Start Menu folder does not exist.")

def remove_desktop_shortcut():
    desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    shortcut_path = os.path.join(desktop_path, DESKTOP_SHORTCUT_NAME)

    # Remove the desktop shortcut if it exists
    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)
        print(f"Removed desktop shortcut: {shortcut_path}")
    else:
        print("Desktop shortcut does not exist.")

def uninstall_application():
    # Remove the Start Menu folder and the desktop shortcut
    remove_start_menu_shortcut()
    remove_desktop_shortcut()

    # Remove the installation directory (remove all files*)
    if os.path.exists(INSTALL_DIR):
        shutil.rmtree(INSTALL_DIR)
        print(f"Removed installation directory: {INSTALL_DIR}")
    else:
        print("Installation directory does not exist.")

if __name__ == "__main__":
    if is_admin():
        uninstall_application()
    else:
        run_as_admin()
