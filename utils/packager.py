import subprocess
import os
import shutil

def build_backend_exe(build_dir):
    launcher_py = os.path.join(build_dir, "launch_backend.py")
    subprocess.run(["pyinstaller", "--onefile", launcher_py], check=True)

    exe_path = os.path.join("dist", "launch_backend.exe")
    electron_dir = os.path.join(build_dir, "electron_app")
    shutil.move(exe_path, os.path.join(electron_dir, "launch_backend.exe"))

def build_electron_app(build_dir):
    electron_dir = os.path.join(build_dir, "electron_app")
    subprocess.run(["npm", "install"], cwd=electron_dir, check=True)
    subprocess.run(["npx", "electron-builder", "--win", "--x64"], cwd=electron_dir, check=True)
