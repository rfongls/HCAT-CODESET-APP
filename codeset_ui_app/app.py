import streamlit as st
from components.file_parser import load_workbook
from components.sheet_tabs import render_sheet_tabs
from utils.dependency_setup import ensure_installed


def load_local_css():
    """Load custom CSS for theming."""
    try:
        with open("codeset_ui_app/assets/styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass


def main() -> None:
    ensure_installed()
    st.set_page_config(page_title="Codeset Automation App", layout="wide")
    load_local_css()
    st.title("Codeset Automation App")

    uploaded_file = st.file_uploader("Upload Codeset Workbook", type=["xlsx"])

    if uploaded_file:
        workbook = load_workbook(uploaded_file)
        render_sheet_tabs(workbook)


if __name__ == "__main__":
    main()
