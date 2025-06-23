import os
from zipfile import ZipFile

def create_wrapper(project_path, framework):
    build_dir = os.path.join(project_path, "desktop_build")
    os.makedirs(build_dir, exist_ok=True)

    # Detect entry
    if framework.lower() == "django":
        entry_script = "manage.py"
        command = f"python {entry_script} runserver 8501"
    elif framework.lower() == "streamlit":
        entry_script = "app.py"
        command = f"streamlit run {entry_script} --server.port 8501"
    else:
        raise ValueError("❌ Only Django and Streamlit are supported.")

    # Find entry path
    entry_path = None
    for root, _, files in os.walk(project_path):
        if entry_script in files:
            entry_path = os.path.join(root, entry_script)
            break
    if not entry_path:
        raise FileNotFoundError(f"❌ {entry_script} not found.")

    entry_dir = os.path.dirname(entry_path)
    full_command = f"cd {entry_dir} && {command}"

    # Launcher script
    launcher_py = os.path.join(build_dir, "launch_backend.py")
    with open(launcher_py, "w") as f:
        f.write(f"""
import subprocess
import threading
import time
def start_server():
    subprocess.Popen(r'''{full_command}''', shell=True)
threading.Thread(target=start_server).start()
time.sleep(3)
""")

    # Electron app
    electron_dir = os.path.join(build_dir, "electron_app")
    os.makedirs(electron_dir, exist_ok=True)

    main_js = """
const { app, BrowserWindow } = require('electron')
const { execFile } = require('child_process')
const path = require('path')

function createWindow () {
  const win = new BrowserWindow({
    width: 1024,
    height: 768
  })
  win.loadURL('http://localhost:8501')
}

app.whenReady().then(() => {
  const exePath = path.join(__dirname, 'launch_backend.exe')
  execFile(exePath)
  createWindow()
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit()
})
"""

    package_json = """
{
  "name": "chatbot-desktop",
  "version": "1.0.0",
  "main": "main.js",
  "scripts": {
    "start": "electron .",
    "build": "electron-builder --win --x64"
  },
  "build": {
    "appId": "com.chatbot.desktop",
    "files": [
      "**/*"
    ],
    "extraResources": [
      "launch_backend.exe"
    ]
  }
}
"""

    with open(os.path.join(electron_dir, "main.js"), "w") as f:
        f.write(main_js)

    with open(os.path.join(electron_dir, "package.json"), "w") as f:
        f.write(package_json)

    # Optional zip
    zip_path = os.path.join(project_path, "desktop_build.zip")
    with ZipFile(zip_path, "w") as zipf:
        for root, _, files in os.walk(build_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, build_dir)
                zipf.write(full_path, rel_path)

    return build_dir
