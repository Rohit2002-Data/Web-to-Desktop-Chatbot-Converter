import os
import shutil
import subprocess
from zipfile import ZipFile

def package_app(project_path, framework):
    desktop_dir = os.path.join(project_path, "desktop_build")
    os.makedirs(desktop_dir, exist_ok=True)

    # Example: if it's a Django app, create run_server.py
    with open(os.path.join(desktop_dir, "run_server.py"), "w") as f:
        f.write("import os\nos.system('python manage.py runserver')")

    # Use PyInstaller to generate executable
    subprocess.run(["pyinstaller", "--onefile", "run_server.py"], cwd=desktop_dir)

    # Zip result
    output_zip = os.path.join(project_path, "ChatbotApp.zip")
    with ZipFile(output_zip, "w") as zipf:
        for root, _, files in os.walk(desktop_dir):
            for file in files:
                if file.endswith(".exe") or file == "run_server.py":
                    zipf.write(os.path.join(root, file), arcname=file)
    return output_zip
