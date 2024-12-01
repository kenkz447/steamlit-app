import time
import re
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_local_storage import LocalStorage
from streamlit_js_eval import streamlit_js_eval

import libs.scanner as scanner

localS = LocalStorage()
query_params = st.query_params

auto_start = query_params.get('auto_start') == 'True'
if auto_start:
    st.session_state.update(started=True)

st.write('___')
st.write(f'Welcome *{st.session_state["name"]}*')
st.title('Data scanner')    
st.write('___')

is_started = st.session_state.get("started", False)

url_template = st.text_input("Url", query_params.get('url_template') or '', disabled=is_started, key="url_template")

id_regex = r"{{ID:(\d*)}}"

def stop():
    query_params.pop('auto_start', None)
    st.session_state.update(started=False)

def get_id(url):
    match = re.findall(id_regex, url)
    if match:
        return match[0]
    return None

def validate_url(url):
    if not re.match(r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+", url):
        st.error("Invalid URL")
        return False
    id = get_id(url)
    if not id:
        st.error("Url must contain {{ID:<number>}}")
        return False
    return True

is_valid_url = validate_url(url_template)

if(not is_started):
    st.button("Start", key="start", disabled=not is_valid_url, on_click=lambda: st.session_state.update(started=True))
else:
    st.button("Stop", key="stop", on_click=stop)

stored_results = localS.getItem("results") or []

def results_to_df(results):
    return pd.DataFrame(results, columns=['id', 'name', 'mobile'])

placeholder = st.empty()

with placeholder.container():
    d = results_to_df(stored_results)
    df = pd.DataFrame(pd.DataFrame(data=d), columns=['id', 'name', 'mobile'])
    st.table(df)
    st.button("Clear table", on_click=lambda: localS.setItem("results", []))

if is_started:
    global result
    result = None

    while result is None:
        id = get_id(url_template)
        url = re.sub(id_regex, id, url_template)

        scanner_profile = scanner.ScannerProfile()
        scanner_profile.url = url
        scanner_profile.fields = {
            "name": "#content > div:nth-child(6) > div.col-md-8 > div.row > div.col-xs-7 > div > div.col-xs-9 > div.name",
            "mobile": "#content > div:nth-child(6) > div.col-md-8 > div.row > div.col-xs-5 > div:nth-child(1) > div.col-xs-8"
        }

        result = scanner.run_scanner(scanner_profile)
        result.update(id=id)
        time.sleep(1)
    
    stored_results.append(result)
    localS.setItem("results", stored_results)
    next_id = int(id) + 1
    next_url = url_template.replace(id, str(next_id))
    st.query_params.update(url_template=next_url, auto_start=True)
    streamlit_js_eval(js_expressions="parent.window.location.reload()")