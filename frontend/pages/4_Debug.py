import os
import streamlit as st
import openai
import pandas as pd
import time
import pyodbc
# from util import PostgresqlConnector, MSAccessConnector
from util.connectors import PostgresqlConnector, MSAccessConnector
st.session_state.update(st.session_state)
st.write(str(st.session_state))
st.write(PostgresqlConnector('localhost',5432,'postgres','postgres','postgres').list_tables())
st.write(MSAccessConnector('C:\workdir\poc\GenAI\Test1.accdb').list_tables())