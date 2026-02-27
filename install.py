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

def search_files(directory, extension):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(extension):
                files.append(os.path.join(root, filename))
    return files

# Get the username of the account
username = getpass.getuser()

# Directory to search within
directory_to_search = f'/home/{username}'

# Search for snake.png
snake_png = search_files(directory_to_search, 'snake.png')

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
    desktop_entry_file = f'/home/{username}/.local/share/applications/snake.desktop'
    destination_dir = f'/home/{username}/.local/share/applications/snake/'

    # Create the necessary directories
    os.makedirs(destination_dir, exist_ok=True)

    # Copy the snake.png file to the destination directory
    for file in snake_png:
        filename = os.path.basename(file)
        destination = os.path.join(destination_dir, filename)
        shutil.copy2(file, destination)

    with open(desktop_entry_file, 'w') as f:
        f.write(desktop_entry)

    # Set execute permissions on the desktop entry file
    os.chmod(desktop_entry_file, 0o755)

# Run the create_desktop_entry() function to create the desktop entry
create_desktop_entry()
print('Snake has been successfully installed!')

sys.exit(0)