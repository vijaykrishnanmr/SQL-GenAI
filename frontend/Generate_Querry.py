import os
import streamlit as st
import openai
import pandas as pd
import time
import pyodbc
# from util import PostgresqlConnector, MSAccessConnector
from util.connectors import PostgresqlConnector, MSAccessConnector
st.session_state.update(st.session_state)


# Configure OpenAI
openai.api_type = "azure"
openai.api_base = "https://generativetesing12.openai.azure.com/"
openai.api_version = "2022-12-01"
openai.api_key = "7b6053efd02247279c877b52fd78ff36"

st.set_page_config(page_title="SQL Query Generator", page_icon="nttdata.png", layout="centered", initial_sidebar_state="collapsed", menu_items=None)
if 'profiles' not in st.session_state:
    st.session_state['profiles'] = ['Postgresql','MS Access']
for profile in st.session_state['profiles']:
    if profile not in st.session_state:
        st.session_state[profile] = None
# Streamlit app
             
generated_query = ""
try:
    st.selectbox("Select database profile",st.session_state.profiles,key='selected_profile')
    user_input = st.text_input("Enter a natural language query:",key="natural_querry")
    sqlquery_prompt = f"Generate  an {st.session_state['selected_profile'] if not st.session_state[st.session_state['selected_profile']] else st.session_state[st.session_state['selected_profile']].type} sql query :{user_input}"

    # Generate query
    if user_input and st.button("Generate SQL Query"):
        response = openai.Completion.create(
            engine="maltext",
            prompt=sqlquery_prompt,
            temperature=1,
            max_tokens=350,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            best_of=1,
            stop=None
        )
        
        # Extract generated email from response
        generated_query = response.choices[0].text.strip()
        st.write("Generated SQL Query")
        st.code(generated_query)
        conn_object = st.session_state[st.session_state["selected_profile"]]
        if conn_object:
            with st.spinner("Getting queery results..."):
                try:
                    df = conn_object.get_results(generated_query)
                    st.write("Query Results:")
                    st.dataframe(df)

                except pyodbc.Error as e:
                    st.write(f"Error executing SQL query: {str(e)}")
            st.success("Querry results processed!")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")


