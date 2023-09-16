import os
import streamlit as st
try:
    import pandas as pd
    import time
    # from util import PostgresqlConnector, MSAccessConnector
    from util.connectors import PostgresqlConnector
except Exception as e:
    st.error(f"Import error:{e}")
st.session_state.update(st.session_state)

try:
# st page structure
    st.set_page_config(page_title="Database Profile Configuration", page_icon="nttdata.png", layout="centered", initial_sidebar_state="collapsed", menu_items=None)

    name = st.text_input("Name")
    hostname = st.text_input("Hostname")
    port = st.text_input("Port")
    username = st.text_input("Username")
    password = st.text_input("Password",type='password')
    database = st.text_input("Database")
    submitted = st.button("Submit")
    if submitted:
        st.session_state.profiles.append(name)
        st.session_state[name] = PostgresqlConnector(hostname,port,username,password,database)
        st.write(f"{st.session_state.profiles} created!!")
except Exception as e:
    st.error(f"Database config : {e}")

