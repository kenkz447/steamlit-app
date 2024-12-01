import streamlit as st

import libs.auth as auth

try:
    auth.authenticator.login()
except Exception as e:
    st.error(e)
