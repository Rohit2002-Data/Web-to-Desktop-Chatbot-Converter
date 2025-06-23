import subprocess
import os
import shutil

def build_backend_exe(build_dir):
    launcher_py = os.path.join(build_dir, "launch_backend.py")

    # Run pyinstaller inside build_dir so dist is in a known location
    subprocess.run(["pyinstaller", "--onefile", launcher_py], cwd=build_dir, check=True)

    dist_dir = os.path.join(build_dir, "dist")
    exe_path = os.path.join(dist_dir, "launch_backend.exe")

    if not os.path.exists(exe_path):
        raise FileNotFoundError(f"Could not find exe at {exe_path}")

    electron_dir = os.path.join(build_dir, "electron_app")
    shutil.move(exe_path, os.path.join(electron_dir, "launch_backend.exe"))

    # Optional: clean up build and spec files
    shutil.rmtree(os.path.join(build_dir, "build"), ignore_errors=True)
    os.remove(os.path.join(build_dir, "launch_backend.spec"))

def build_electron_app(build_dir):
    electron_dir = os.path.join(build_dir, "electron_app")

    # Install dependencies
    subprocess.run(["npm", "install"], cwd=electron_dir, check=True)

    # Build the Electron installer
    subprocess.run(["npx", "electron-builder", "--win", "--x64"], cwd=electron_dir, check=True)

