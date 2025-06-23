import streamlit as st
from utils.file_handler import handle_upload
from utils.framework_detector import detect_framework
from utils.executor import run_chatbot
from utils.wrapper_generator import create_wrapper
from utils.packager import build_backend_exe, build_electron_app

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

    if st.button("🖥 Convert to Desktop Installer"):
        build_dir = create_wrapper(app_dir, framework)
        st.success("✅ Desktop app structure created!")

        build_backend_exe(build_dir)
        st.success("✅ Backend .exe built!")

        build_electron_app(build_dir)
        st.success("🎉 Installer built! Check: desktop_build/electron_app/dist/")
