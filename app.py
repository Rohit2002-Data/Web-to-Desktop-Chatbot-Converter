import streamlit as st
from utils.analyzer import detect_framework
from utils.packager import package_app
from utils.file_handler import handle_upload

st.title("🤖 Web Chatbot → Desktop App Converter")

uploaded_file = st.file_uploader("Upload your chatbot web app (ZIP)", type=["zip"])

if uploaded_file:
    project_path = handle_upload(uploaded_file)
    st.success("✅ Uploaded and extracted!")

    framework = detect_framework(project_path)
    st.info(f"Detected framework: **{framework}**")

    if st.button("Convert to Desktop App"):
        with st.spinner("Packaging your app..."):
            output_path = package_app(project_path, framework)
            st.success("🎉 Conversion complete!")
            st.download_button("Download Desktop App", open(output_path, "rb"), file_name="ChatbotApp.zip")
