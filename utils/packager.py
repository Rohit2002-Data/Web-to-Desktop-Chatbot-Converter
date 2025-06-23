import subprocess
import os
import shutil

def build_backend_exe(build_dir):
    launcher_py = os.path.join(build_dir, "launch_backend.py")

    try:
        # Run pyinstaller in build_dir so dist/ lands in a known place
        result = subprocess.run(
            ["pyinstaller", "--onefile", launcher_py],
            cwd=build_dir,
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ PyInstaller STDOUT:")
        print(result.stdout)
        print("✅ PyInstaller STDERR (if any):")
        print(result.stderr)

    except subprocess.CalledProcessError as e:
        print("❌ PyInstaller failed!")
        print("=== STDOUT ===")
        print(e.stdout)
        print("=== STDERR ===")
        print(e.stderr)
        raise RuntimeError("PyInstaller build failed. See output above.") from e

    # Find the exe
    dist_dir = os.path.join(build_dir, "dist")
    exe_path = os.path.join(dist_dir, "launch_backend.exe")

    if not os.path.exists(exe_path):
        raise FileNotFoundError(f"❌ Could not find exe at {exe_path}")

    # Move to electron folder
    electron_dir = os.path.join(build_dir, "electron_app")
    shutil.move(exe_path, os.path.join(electron_dir, "launch_backend.exe"))

    # Cleanup
    shutil.rmtree(os.path.join(build_dir, "build"), ignore_errors=True)
    spec_file = os.path.join(build_dir, "launch_backend.spec")
    if os.path.exists(spec_file):
        os.remove(spec_file)

def build_electron_app(build_dir):
    electron_dir = os.path.join(build_dir, "electron_app")

    try:
        print("⚙ Running npm install...")
        subprocess.run(["npm", "install"], cwd=electron_dir, check=True, capture_output=True, text=True)
        print("⚙ Running electron-builder...")
        subprocess.run(["npx", "electron-builder", "--win", "--x64"], cwd=electron_dir, check=True, capture_output=True, text=True)
        print("✅ Electron app built successfully!")

    except subprocess.CalledProcessError as e:
        print("❌ Electron build failed!")
        print("=== STDOUT ===")
        print(e.stdout)
        print("=== STDERR ===")
        print(e.stderr)
        raise RuntimeError("Electron build failed. See output above.") from e
