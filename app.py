import streamlit as st 

chat_page = st.Page("chat_page.py", title="Chat", icon="💬")
about_page = st.Page("about_page.py", title="About", icon="ℹ️")

pg = st.navigation([chat_page, about_page])

pg.run()