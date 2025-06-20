import os
import subprocess
from zipfile import ZipFile

def create_wrapper(project_path, framework):
    """
    Converts a web chatbot project into a desktop app launcher.
    If on Windows, builds a .exe using PyInstaller.
    On other systems, packages a Python launcher with the full chatbot project.
    Returns the path to the output ZIP file.
    """
    build_dir = os.path.join(project_path, "desktop_build")
    os.makedirs(build_dir, exist_ok=True)

    # Determine main entry point and command
    if framework == "Django":
        entry_script = "manage.py"
        command = f"python {entry_script} runserver"
    elif framework == "Flask":
        entry_script = "app.py"
        command = f"python {entry_script}"
    elif framework == "Streamlit":
        entry_script = "app.py"
        command = f"streamlit run {entry_script}"
    else:
        raise ValueError("Unsupported framework")

    # Locate full path to entry script
    entry_path = None
    for root, _, files in os.walk(project_path):
        if entry_script in files:
            entry_path = os.path.join(root, entry_script)
            break

    if not entry_path:
        raise FileNotFoundError(f"{entry_script} not found.")

    # Create launcher script
    launcher_script = os.path.join(build_dir, "launch_chatbot.py")
    with open(launcher_script, "w") as f:
        f.write(f"import os\nos.system(r'''{command}''')")

    output_zip = os.path.join(project_path, "chatbot_desktop_app.zip")
    dist_dir = os.path.join(build_dir, "dist")

    try:
        if os.name == "nt":  # Build .exe only on Windows
            subprocess.run(["pyinstaller", "--onefile", launcher_script], cwd=build_dir, check=True)

            if not os.path.exists(dist_dir):
                raise FileNotFoundError("PyInstaller did not create /dist folder")

            exe_files = [f for f in os.listdir(dist_dir) if f.endswith(".exe")]
            if not exe_files:
                raise FileNotFoundError("No .exe file generated.")

            # Create zip with .exe
            with ZipFile(output_zip, "w") as zipf:
                for file in exe_files:
                    zipf.write(os.path.join(dist_dir, file), arcname=file)

        else:
            # On Linux/macOS: include launcher and chatbot project
            with ZipFile(output_zip, "w") as zipf:
                zipf.write(launcher_script, arcname="launch_chatbot.py")

                for foldername, subfolders, filenames in os.walk(project_path):
                    for filename in filenames:
                        filepath = os.path.join(foldername, filename)
                        arcname = os.path.relpath(filepath, project_path)
                        if "desktop_build" not in arcname and not arcname.endswith(".zip"):
                            zipf.write(filepath, arcname=arcname)

    except Exception as e:
        raise RuntimeError(f"Desktop app build failed: {str(e)}")

    return output_zip
