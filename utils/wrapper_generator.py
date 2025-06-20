import os
import subprocess
from zipfile import ZipFile

def create_wrapper(project_path, framework):
    build_dir = os.path.join(project_path, "desktop_build")
    os.makedirs(build_dir, exist_ok=True)

    # Detect entry script and command
    if framework == "Django":
        entry_script = "manage.py"
        command = f"python {entry_script} runserver"
    else:
        raise ValueError("Only Django is supported in this project.")

    # Find full path to manage.py
    entry_path = None
    for root, _, files in os.walk(project_path):
        if entry_script in files:
            entry_path = os.path.join(root, entry_script)
            break

    if not entry_path:
        raise FileNotFoundError(f"{entry_script} not found.")

    # Set working directory to location of manage.py
    entry_dir = os.path.dirname(entry_path)
    command_full = f"cd {entry_dir} && {command}"

    # Create launcher script
    launcher_script = os.path.join(build_dir, "launch_chatbot.py")
    with open(launcher_script, "w") as f:
        f.write(f"import os\nos.system(r'''{command_full}''')")

    # Output zip path
    output_zip = os.path.join(project_path, "chatbot_desktop_app.zip")
    dist_dir = os.path.join(build_dir, "dist")

    try:
        if os.name == "nt":  # Windows system
            subprocess.run(["pyinstaller", "--onefile", launcher_script], cwd=build_dir, check=True)

            if not os.path.exists(dist_dir):
                raise FileNotFoundError("PyInstaller did not create /dist folder")

            exe_files = [f for f in os.listdir(dist_dir) if f.endswith(".exe")]
            if not exe_files:
                raise FileNotFoundError("No .exe file generated.")

            with ZipFile(output_zip, "w") as zipf:
                for file in exe_files:
                    zipf.write(os.path.join(dist_dir, file), arcname=file)
        else:
            # Linux/macOS fallback: just zip the launcher script
            with ZipFile(output_zip, "w") as zipf:
                zipf.write(launcher_script, arcname="launch_chatbot.py")

    except Exception as e:
        raise RuntimeError(f"Desktop app build failed: {str(e)}")

    return output_zip
