import time
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_local_storage import LocalStorage
from streamlit_js_eval import streamlit_js_eval

from libs.profiles import select_profile
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
sites = ["bds.com.vn", "bannha888", "nhadat.cafeland.vn", "nhadat24h.net", "mogi.vn"]
site_id = st.selectbox(
    "Site",
    index=sites.index(query_params.get('site_id') or "bds.com.vn") ,
    options=sites,
    disabled=is_started)
user_id = st.number_input("Id", value=int(query_params.get('id') or 0), disabled=is_started)

def stop():
    query_params.pop('auto_start', None)
    st.session_state.update(started=False)

if(not is_started):
    st.button("Start", key="start", disabled=user_id == 0, on_click=lambda: st.session_state.update(started=True))
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
    st.button("Clear table", disabled=is_started, on_click=lambda: localS.setItem("results", []))

if is_started:
    global result
    result = None

    placeholderError = st.empty()
    retry = 0
    while result is None:
        scanner_profile = select_profile(site_id, user_id)
        try:
            result = scanner.run_scanner(scanner_profile)
            result.update(id=user_id)
            continue
        except Exception as e:
            with placeholderError.container():
                st.error(f"(Retry: {retry}) Error: {e}")
        retry += 1
        random_sleep = np.random.randint(5, 10)
        time.sleep(random_sleep)
    
    stored_results.append(result)
    localS.setItem("results", stored_results)
    next_id = int(user_id) + 1
    st.query_params.update(site_id=site_id, id=next_id, auto_start=True)
    streamlit_js_eval(js_expressions="parent.window.location.reload()")