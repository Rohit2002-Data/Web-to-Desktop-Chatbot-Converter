import os
import subprocess
import shutil
from zipfile import ZipFile

def create_wrapper(project_path, framework):
    if not os.path.exists(project_path):
        raise FileNotFoundError(f"❌ Project path does not exist: {project_path}")

    build_dir = os.path.join(project_path, "desktop_build")
    os.makedirs(build_dir, exist_ok=True)

    # Detect entry script and command based on framework
    if framework.lower() == "django":
        entry_script = "manage.py"
        command = f"python {entry_script} runserver 8501"
    elif framework.lower() == "streamlit":
        entry_script = "app.py"
        command = f"streamlit run {entry_script} --server.port 8501"
    else:
        raise ValueError("❌ Only Django and Streamlit are supported.")

    # Locate the entry script
    entry_path = None
    for root, _, files in os.walk(project_path):
        if entry_script in files:
            entry_path = os.path.join(root, entry_script)
            break

    if not entry_path:
        raise FileNotFoundError(f"❌ {entry_script} not found in project.")

    entry_dir = os.path.dirname(entry_path)
    full_command = f"cd {entry_dir} && {command}"

    # Create launcher Python script to start backend server
    launcher_script = os.path.join(build_dir, "launch_backend.py")
    with open(launcher_script, "w") as f:
        f.write("import subprocess\n")
        f.write("import threading\n")
        f.write("import webbrowser\n")
        f.write("import time\n\n")
        f.write("def start_server():\n")
        f.write(f"    subprocess.Popen(r'''{full_command}''', shell=True)\n\n")
        f.write("threading.Thread(target=start_server).start()\n")
        f.write("time.sleep(3)\n")
        f.write("webbrowser.open('http://localhost:8501')\n")

    # Create Electron app directory
    electron_dir = os.path.join(build_dir, "electron_app")
    os.makedirs(electron_dir, exist_ok=True)

    main_js = f"""
const {{ app, BrowserWindow }} = require('electron')
function createWindow () {{
  const win = new BrowserWindow({{
    width: 1024,
    height: 768,
    webPreferences: {{
      nodeIntegration: true
    }}
  }})
  win.loadURL('http://localhost:8501')
}}
app.whenReady().then(createWindow)
app.on('window-all-closed', () => {{
  if (process.platform !== 'darwin') app.quit()
}})
"""

    package_json = """
{
  "name": "chatbot-desktop",
  "version": "1.0.0",
  "main": "main.js",
  "scripts": {
    "start": "electron ."
  }
}
"""

    # Write Electron files
    with open(os.path.join(electron_dir, "main.js"), "w") as f:
        f.write(main_js)

    with open(os.path.join(electron_dir, "package.json"), "w") as f:
        f.write(package_json)

    # Copy launcher backend script into Electron app
    shutil.copy(launcher_script, os.path.join(electron_dir, "launch_backend.py"))

    # Write shell script to run both backend and Electron app
    run_script = os.path.join(build_dir, "run_desktop_app.sh")
    with open(run_script, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("cd electron_app\n")
        f.write("python3 launch_backend.py &\n")
        f.write("npm install electron --save-dev\n")
        f.write("npx electron .\n")

    # Optional: Windows batch file
    run_bat = os.path.join(build_dir, "run_desktop_app.bat")
    with open(run_bat, "w") as f:
        f.write("cd electron_app\n")
        f.write("start python launch_backend.py\n")
        f.write("npx electron .\n")

    # Zip the entire desktop build folder
    output_zip = os.path.join(project_path, "chatbot_desktop_app_electron.zip")
    with ZipFile(output_zip, "w") as zipf:
        for root, _, files in os.walk(build_dir):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, build_dir)
                zipf.write(full_path, arcname=arcname)

    return output_zip
