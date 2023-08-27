import requests
import streamlit as st


def fetch_data_from_api(url):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            return data
        except:
            return data
    else:
        st.warning("Data Not Found.")
        return []
