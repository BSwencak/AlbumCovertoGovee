import sys, os, subprocess, psutil

action = sys.argv[1]

project_root = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

PID_FILE = os.path.join(
    project_root,
    "spotify.pid"
)

if action == "start":

    if os.path.exists(PID_FILE):
        print("Spotify mode already running.")
        sys.exit()

    subprocess.Popen(
    ["pythonw", os.path.join(project_root, "main.py")],
    cwd=project_root, creationflags=subprocess.CREATE_NO_WINDOW
    )

elif action == "stop":

    if not os.path.exists(PID_FILE):
        print("Spotify mode is not running.")
        sys.exit()

    with open(PID_FILE) as f:
        pid = int(f.read())

    try:
        process = psutil.Process(pid)
        process.terminate()
        process.wait(timeout=5)

    except psutil.NoSuchProcess:
        pass

    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)

    subprocess.run(
        [
            "pythonw",
            r"G:\PC LOCAL DEV\StreamDeck-Govee-Light-Controller-MEONLY\light_controller.py",
            "warm"
        ], creationflags=subprocess.CREATE_NO_WINDOW
    )