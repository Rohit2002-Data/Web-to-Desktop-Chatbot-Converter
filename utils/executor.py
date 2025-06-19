import os
import subprocess

def run_chatbot(project_path, framework):
    """
    Starts the chatbot web application depending on the detected framework.
    Looks for the correct entry point even in nested folders.
    """
    # Recursively search for the run file
    run_file = None
    for root, dirs, files in os.walk(project_path):
        if framework == 'Django' and 'manage.py' in files:
            run_file = os.path.join(root, 'manage.py')
            cmd = ['python', run_file, 'runserver']
            break
        elif framework == 'Flask' and 'app.py' in files:
            run_file = os.path.join(root, 'app.py')
            cmd = ['python', run_file]
            break
        elif framework == 'Streamlit' and 'app.py' in files:
            run_file = os.path.join(root, 'app.py')
            cmd = ['streamlit', 'run', run_file]
            break
        elif framework == 'Streamlit' and 'streamlit_app.py' in files:
            run_file = os.path.join(root, 'streamlit_app.py')
            cmd = ['streamlit', 'run', run_file]
            break

    if run_file is None:
        raise ValueError("Could not locate the entry point script for the selected framework.")

    # Start the web server as a subprocess
    subprocess.Popen(cmd, cwd=os.path.dirname(run_file))
