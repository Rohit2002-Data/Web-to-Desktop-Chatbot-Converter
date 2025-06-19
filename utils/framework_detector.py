import os

def detect_framework(project_path):
    files = os.listdir(project_path)
    if 'manage.py' in files:
        return 'Django'
    elif 'app.py' in files or 'main.py' in files:
        return 'Flask'
    elif 'streamlit_app.py' in files or 'app.py' in files:
        return 'Streamlit'
    else:
        return 'Unknown'