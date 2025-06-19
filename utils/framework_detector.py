import os

def detect_framework(project_path):
    """
    Recursively detect the web framework used in the uploaded project.
    Returns one of: 'Django', 'Flask', 'Streamlit', or 'Unknown'.
    """
    for root, dirs, files in os.walk(project_path):
        if 'manage.py' in files:
            return 'Django'
        elif 'app.py' in files or 'main.py' in files:
            # Distinguish between Streamlit and Flask
            app_file = os.path.join(root, 'app.py')
            if os.path.exists(app_file):
                with open(app_file, 'r') as f:
                    content = f.read()
                    if 'streamlit' in content.lower():
                        return 'Streamlit'
                    elif 'flask' in content.lower():
                        return 'Flask'
            return 'Flask'
        elif 'streamlit_app.py' in files:
            return 'Streamlit'

    return 'Unknown'
