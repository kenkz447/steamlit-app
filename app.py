import streamlit as st

from libs.auth import check_login_status

import os
os.system("playwright install")

page_login = st.Page("routes/login.py")
page_agents = st.Page("routes/agents.py")

if check_login_status():
    pg = st.navigation([page_agents])
else:
    pg = st.navigation([page_login])

pg.run()