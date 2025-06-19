import os
import shutil
import subprocess
from zipfile import ZipFile

def create_wrapper(project_path, framework):
    build_dir = os.path.join(project_path, "build")
    os.makedirs(build_dir, exist_ok=True)

    if framework == 'Streamlit':
        entry_script = 'app.py'
    elif framework == 'Django':
        entry_script = 'manage.py'
    elif framework == 'Flask':
        entry_script = 'app.py'
    else:
        raise ValueError("Unsupported framework")

    # Create launcher script
    launcher_path = os.path.join(build_dir, 'launch.py')
    with open(launcher_path, 'w') as f:
        f.write(f"import os\nos.system('python {entry_script}')")

    # Run PyInstaller
    subprocess.run(["pyinstaller", "--onefile", launcher_path], cwd=build_dir)

    dist_path = os.path.join(build_dir, "dist")
    output_zip = os.path.join(project_path, "chatbot_desktop.zip")

    with ZipFile(output_zip, 'w') as zipf:
        for root, _, files in os.walk(dist_path):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=file)

    return output_zip
