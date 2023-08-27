from uuid import uuid4

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


st.set_page_config(layout="wide")
st.title("Chat")


if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid4())

query_params = st.experimental_get_query_params()
# st.write(query_params)


data = fetch_data_from_api(f"{setting.API_ENDPOINT}/api/data/")

try:
    title = query_params.get("title")[0]
    selected_items = st.sidebar.multiselect(
        "Select a data",
        options=[item["title"] for item in data],
        default=title,
        format_func=lambda item: item,
    )
except Exception:
    selected_items = st.sidebar.multiselect(
        "Select a data",
        options=[item["title"] for item in data],
        default=None,
        format_func=lambda item: item,
    )

for selected_item in selected_items:
    selected_data = next(
        (item for item in data if item["title"] == selected_item), None
    )
    if selected_data:
        st.sidebar.write(f"**Type:** {selected_data['type']}")
        st.sidebar.write(f"**Source:** {selected_data['source']}")
        st.sidebar.write(f"**Status:** {selected_data['status']}")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Hello?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Add loading state
        loading_placeholder = st.empty()

        with st.spinner("Thinking..."):
            response = requests.get(
                f"{setting.API_ENDPOINT}/api/ask/vector-memory",
                params={
                    "title": selected_data["title"],
                    "question": prompt,
                    "stream": "true",
                    "session_id": st.session_state.session_id,
                },
            )
            json_response = response.json()
            full_response = json_response.get("answer", "")
            loading_placeholder.empty()

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                message_placeholder.markdown(full_response + "▌")

            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )
