import sys, os, subprocess, psutil
import subprocess

action = sys.argv[1]


if action == "start":

    if os.path.exists("spotify.pid"):
        print("Spotify mode already running.")
        sys.exit()

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    subprocess.Popen(
        ["python", os.path.join(project_root, "main.py")]
    )

elif action == "stop":

    if not os.path.exists("spotify.pid"):
        print("Spotify mode is not running.")
        sys.exit()

    with open("spotify.pid") as f:
        pid = int(f.read())

    try:
        
        psutil.Process(pid).terminate()
    except psutil.NoSuchProcess:
        pass