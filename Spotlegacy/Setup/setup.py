#Make identical to spotify setup ;))

import os
import zipfile
import requests
import subprocess
from tkinter import Tk, Label, Button, StringVar, DoubleVar, ttk, Toplevel
from io import BytesIO
import win32com.client
import ctypes
import sys

DOWNLOAD_URL = 'http://example.com/SpotLegacy_Old_UI_(Patched_Premium).zip' #Download link zip
APPDATA_DIR = os.getenv('APPDATA')  # Path to %AppData%
INSTALL_DIR = os.path.join(APPDATA_DIR, 'Spotify')
EXECUTABLE_NAME = 'Spotify.exe'  # Executable
START_MENU_FOLDER = 'Spotify'  # folder in Start Menu

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

class InstallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spotlegacy Installer")

        # Prevent resizing of the window
        self.root.resizable(False, False)

        self.status_var = StringVar()
        self.progress_var = DoubleVar()

        self.status_label = Label(root, textvariable=self.status_var)
        self.status_label.pack(pady=5)
        self.progress_bar = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate', variable=self.progress_var)
        self.progress_bar.pack(pady=10)

        # Start installation automatically
        self.root.after(100, self.start_installation)  # Delay

    def start_installation(self):
        """Start the installation process."""
        # Step 1: Download the file
        self.status_var.set("Downloading Spotlegacy")
        self.root.update()
        try:
            self.download_and_extract(DOWNLOAD_URL, INSTALL_DIR)
            
            # Step 2: Installation
            self.status_var.set("Installing Spotlegacy")
            self.progress_var.set(0)  # Reset the progress bar
            self.root.update()
            self.create_shortcuts()
            
            # Installation Complete
            self.status_var.set("Installation Complete")
            self.progress_var.set(100)
            self.root.after(2000, self.launch_application)  # Launch application after 2 seconds
        except Exception as e:
            self.show_error_window(str(e))

    def download_and_extract(self, url, extract_to):
        """Download and extract the ZIP file."""
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        chunk_size = 8192
        downloaded_size = 0

        with BytesIO() as zip_buffer:
            for chunk in response.iter_content(chunk_size=chunk_size):
                zip_buffer.write(chunk)
                downloaded_size += len(chunk)
                self.progress_var.set((downloaded_size / total_size) * 100)
                self.root.update()

            zip_buffer.seek(0)
            with zipfile.ZipFile(zip_buffer) as zip_file:
                if not os.path.exists(extract_to):
                    os.makedirs(extract_to)
                zip_file.extractall(extract_to)

    def create_shortcuts(self):
        """Create shortcuts for the application."""
        shell = win32com.client.Dispatch("WScript.Shell")

        # Start Menu path
        start_menu_path = shell.SpecialFolders("StartMenu")
        app_folder_path = os.path.join(start_menu_path, START_MENU_FOLDER)

        # Desktop path
        desktop_path = shell.SpecialFolders("Desktop")

        # Create folder in Start Menu if it doesn't exist
        if not os.path.exists(app_folder_path):
            os.makedirs(app_folder_path)

        # Check if executable exists
        executable_path = os.path.join(INSTALL_DIR, EXECUTABLE_NAME)
        if not os.path.isfile(executable_path):
            raise FileNotFoundError(f"The executable file {EXECUTABLE_NAME} was not found in {INSTALL_DIR}")

        # Create a shortcut to the application in Start Menu
        shortcut_path_start_menu = os.path.join(app_folder_path, f'{EXECUTABLE_NAME}.lnk')
        self.create_shortcut(shell, shortcut_path_start_menu, executable_path)

        # Create a shortcut to the application on Desktop
        shortcut_path_desktop = os.path.join(desktop_path, f'{EXECUTABLE_NAME}.lnk')
        self.create_shortcut(shell, shortcut_path_desktop, executable_path)

    def create_shortcut(self, shell, shortcut_path, target_path):
        """Create a shortcut with the application icon."""
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = target_path
        shortcut.WorkingDirectory = os.path.dirname(target_path)
        shortcut.IconLocation = f"{target_path}, 0"  # Set the icon of the executable
        shortcut.save()

    def launch_application(self):
        """Launch the application after installation."""
        app_path = os.path.join(INSTALL_DIR, EXECUTABLE_NAME)
        if os.path.isfile(app_path):
            try:
                subprocess.Popen(app_path)
            except Exception as e:
                self.show_error_window(f"Failed to start the application: {str(e)}")
        else:
            self.show_error_window(f"Application executable not found: {app_path}")
        self.root.destroy()  # Close the installer window after launching the application

    def show_error_window(self, error_message):
        """Display an error window in case of failure."""
        error_window = Toplevel(self.root)
        error_window.title("Error")

        Label(error_window, text="Installation Failed", font=("Arial", 16)).pack(pady=10)
        Label(error_window, text=f"Error: {error_message}", font=("Arial", 12)).pack(pady=10)
        Button(error_window, text="OK", command=self.root.quit).pack(pady=20)

        # Ensure the main window is closed only after showing the error window
        self.root.after(0, self.root.destroy)

if __name__ == "__main__":
    if is_admin():
        root = Tk()
        app = InstallerApp(root)
        root.mainloop()
    else:
        run_as_admin()
