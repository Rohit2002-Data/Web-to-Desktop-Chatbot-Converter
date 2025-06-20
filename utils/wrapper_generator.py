# Enhanced create_wrapper function with Streamlit and Django support, robust error logging, and diagnostic output

import os
import subprocess
from zipfile import ZipFile

def create_wrapper(project_path, framework):
    if not os.path.exists(project_path):
        raise FileNotFoundError(f"❌ Project path does not exist: {project_path}")

    build_dir = os.path.join(project_path, "desktop_build")
    os.makedirs(build_dir, exist_ok=True)

    # Detect entry script and command based on framework
    if framework.lower() == "django":
        entry_script = "manage.py"
        command = f"python {entry_script} runserver"
    elif framework.lower() == "streamlit":
        entry_script = "app.py"
        command = f"streamlit run {entry_script}"
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
    command_full = f"cd {entry_dir} && {command}"

    # Create the launcher script
    launcher_script = os.path.join(build_dir, "launch_chatbot.py")
    with open(launcher_script, "w") as f:
        f.write("import os\n")
        f.write("import subprocess\n")
        f.write(f"subprocess.run(r'''{command_full}''', shell=True)\n")

    # Build with PyInstaller on Windows or fallback to script zip
    output_zip = os.path.join(project_path, "chatbot_desktop_app.zip")
    dist_dir = os.path.join(build_dir, "dist")

    try:
        if os.name == "nt":
            subprocess.run(["pyinstaller", "--onefile", launcher_script], cwd=build_dir, check=True)

            if not os.path.exists(dist_dir):
                raise FileNotFoundError("❌ PyInstaller did not create /dist folder.")

            exe_files = [f for f in os.listdir(dist_dir) if f.endswith(".exe")]
            if not exe_files:
                raise FileNotFoundError("❌ No .exe file generated.")

            with ZipFile(output_zip, "w") as zipf:
                for file in exe_files:
                    zipf.write(os.path.join(dist_dir, file), arcname=file)
        else:
            with ZipFile(output_zip, "w") as zipf:
                zipf.write(launcher_script, arcname="launch_chatbot.py")

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"❌ PyInstaller failed: {e}")
    except Exception as e:
        raise RuntimeError(f"❌ Desktop app build failed: {str(e)}")

    return output_zip

