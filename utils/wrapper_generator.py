import os
import subprocess
from zipfile import ZipFile

def create_wrapper(project_path, framework="Django"):
    build_dir = os.path.join(project_path, "desktop_build")
    os.makedirs(build_dir, exist_ok=True)

    # Write manage.py if missing
    manage_py_path = os.path.join(project_path, "manage.py")
    if not os.path.exists(manage_py_path):
        with open(manage_py_path, "w") as f:
            f.write("""#!/usr/bin/env python
import os, sys
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoprojects.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
""")

    entry_script = "manage.py"
    command = f"python {entry_script} runserver"

    # Create launcher script
    launcher_script = os.path.join(build_dir, "launch_chatbot.py")
    with open(launcher_script, "w") as f:
        f.write(f"import os\nos.chdir(r'{project_path}')\nos.system(r'''{command}''')")

    # Build executable only if on Windows
    output_zip = os.path.join(project_path, "chatbot_desktop_app.zip")
    dist_dir = os.path.join(build_dir, "dist")

    try:
        if os.name == "nt":
            subprocess.run(["pyinstaller", "--onefile", launcher_script], cwd=build_dir, check=True)

            exe_files = [f for f in os.listdir(dist_dir) if f.endswith(".exe")]
            if not exe_files:
                raise FileNotFoundError("No .exe file generated.")

            with ZipFile(output_zip, "w") as zipf:
                for file in exe_files:
                    zipf.write(os.path.join(dist_dir, file), arcname=file)

        else:
            # For Linux/macOS users, zip the script
            with ZipFile(output_zip, "w") as zipf:
                zipf.write(launcher_script, arcname="launch_chatbot.py")

    except Exception as e:
        raise RuntimeError(f"Desktop app build failed: {str(e)}")

    return output_zip
