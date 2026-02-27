import subprocess
import sys

try:
    # Build the package
    subprocess.run([sys.executable, "setup.py", "build"], check=True)

    # Install the package with sudo
    subprocess.run(["sudo", sys.executable, "setup.py", "install"], check=True)

except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
    sys.exit(1)

sys.exit(0)
