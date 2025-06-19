import os
import subprocess

def run_chatbot(project_path, framework):
    if framework == 'Django':
        subprocess.Popen(['python', 'manage.py', 'runserver'], cwd=project_path)
    elif framework == 'Flask':
        subprocess.Popen(['python', 'app.py'], cwd=project_path)
    elif framework == 'Streamlit':
        subprocess.Popen(['streamlit', 'run', 'app.py'], cwd=project_path)
    else:
        raise ValueError("Unsupported framework")
