import streamlit as st
from utils.file_handler import handle_upload
from utils.framework_detector import detect_framework
from utils.executor import run_chatbot
from utils.wrapper_generator import create_wrapper

st.title("🤖 Web Chatbot → Desktop App Converter")

uploaded_file = st.file_uploader("Upload your chatbot web app (ZIP)", type="zip")

if uploaded_file:
    app_dir = handle_upload(uploaded_file)
    st.success("✅ Chatbot uploaded and extracted!")

    framework = detect_framework(app_dir)
    st.info(f"Framework detected: **{framework}**")

    if st.button("▶️ Run Web Chatbot"):
        run_chatbot(app_dir, framework)
        st.success("🚀 Web app running at http://localhost:8000")

    if st.button("🖥 Convert to Desktop App"):
        exe_path = create_wrapper(app_dir, framework)
        st.success("🎉 Desktop app created!")
        with open(exe_path, "rb") as f:
            st.download_button("Download Desktop App", f, file_name="chatbot_desktop.zip")

