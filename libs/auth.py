import streamlit as st

import yaml
import streamlit_authenticator as stauth

from yaml.loader import SafeLoader

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

def init():
    global authenticator

def check_login_status():
    global authenticator
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    
    return st.session_state["authentication_status"]