import os

def detect_framework(project_path):
    if "manage.py" in os.listdir(project_path):
        return "Django"
    elif "app.py" in os.listdir(project_path) or "main.py" in os.listdir(project_path):
        return "Flask"
    elif "streamlit_app.py" in os.listdir(project_path):
        return "Streamlit"
    else:
        return "Unknown"
