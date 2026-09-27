import streamlit as st
from views.dab_view import render_dab_subsection

st.set_page_config(
    page_title="Standard Converters",
    layout="wide",
    page_icon="⚡"
)

# Main Application Branding in Sidebar
st.sidebar.title("⚡ Standard Converters")
st.sidebar.caption("The Standard Converters Project")

# Subsection Navigation Selector
converter_choice = st.sidebar.selectbox(
    "Select Converter Topology",
    options=[
        "DAB Converter",
        "BUCK Converter (Coming Soon)",
        "FLYBACK Converter (Coming Soon)"
    ]
)
st.sidebar.divider()
st.sidebar.caption(
    "Licensed under **AGPLv3** · "
    "[Source Code](https://github.com/Fretizrenaison/standard-converters)"
)

# Route to the selected subsection
if converter_choice == "DAB Converter":
    render_dab_subsection()
else:
    st.info(f"🚧 The **{converter_choice}** module is under development for The Standard Converters Project.")