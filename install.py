import subprocess
import sys
import os
import getpass
import shutil

# Build the package silently
subprocess.run(
    [sys.executable, "setup.py", "build"],
    check=True,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

# Install the package silently with sudo
subprocess.run(
    ["sudo", sys.executable, "setup.py", "install"],
    check=True,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

def search_files(directory, filename):
    """Recursively search for files named `filename` in `directory`."""
    files = []
    for root, _, filenames in os.walk(directory):
        if filename in filenames:
            files.append(os.path.join(root, filename))
    return files

# Get the username of the account
username = getpass.getuser()

# Directory to search within
directory_to_search = f'/home/{username}'

# Search for snake.png
snake_png_files = search_files(directory_to_search, 'snake.png')

def create_desktop_entry():
    desktop_entry = f'''[Desktop Entry]
Type=Application
Name=Snake
Exec=/usr/local/bin/snake
Terminal=false
Icon=/home/{username}/.local/share/applications/snake/snake.png
Categories=Games;
'''

    # Specify the path and filename for the desktop entry file
    destination_dir = f'/home/{username}/.local/share/applications/snake/'
    desktop_entry_file = f'{destination_dir}snake.desktop'

    # Create the necessary directories
    os.makedirs(destination_dir, exist_ok=True)

    # Copy the snake.png file(s) to the destination directory safely
    for file in snake_png_files:
        filename = os.path.basename(file)
        destination = os.path.join(destination_dir, filename)
        # Skip copy if the file already exists at the same path
        if os.path.abspath(file) == os.path.abspath(destination):
            print(f"{filename} already exists at destination, skipping copy.")
            continue
        shutil.copy2(file, destination)

    # Write the desktop entry file
    with open(desktop_entry_file, 'w') as f:
        f.write(desktop_entry)

    # Set execute permissions on the desktop entry file
    os.chmod(desktop_entry_file, 0o755)

# Run the desktop entry creation
create_desktop_entry()
print('Snake has been successfully installed!')

sys.exit(0)