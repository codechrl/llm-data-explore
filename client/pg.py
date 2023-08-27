import requests
import streamlit as st
from setting import setting


def fetch_data_from_api(url):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            return data
        except:
            return data
    else:
        st.error("Failed to fetch data from the API")
        return []


st.subheader("Directory & Files Structure")
selected_data = {"title": "lapisai-query-engine.git"}
# with st.spinner("In progress..."):
#     with st.expander("Tree"):
#         data = fetch_data_from_api(
#             f"{setting.API_ENDPOINT}/api/data/tree?title={selected_data['title']}"
#         )
#         st.markdown(data)

with st.expander("Link"):
    data = fetch_data_from_api(
        f"{setting.API_ENDPOINT}/api/data/tree?title={selected_data['title']}&link=true"
    )
    st.markdown(data)
