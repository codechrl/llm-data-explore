from uuid import uuid4

import requests
import streamlit as st
import streamlit_antd_components as sac
from setting import setting
from streamlit_agraph import Config, Edge, Node, agraph


def fetch_data_from_api(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error("Failed to fetch data from the API")
        return []


def page():
    st.subheader("Article Data!")
    st.session_state.session_id = str(uuid4())

    # Sidebar
    # st.sidebar.header("Youtube Data")
    yotube_url = st.sidebar.text_input("Input web url")
    submit_button = st.sidebar.button("Submit")
    data = fetch_data_from_api(f"{setting.API_ENDPOINT}/api/data/?source=web")
    selected_items = st.sidebar.multiselect(
        "Select a data",
        options=[item["title"] for item in data],
        default=None,
        format_func=lambda item: item,
    )

    if submit_button:
        # Make an HTTP request when the submit button is clicked
        url = f"{setting.API_ENDPOINT}/api/engine/web?background=true&url={yotube_url}"
        response = requests.post(url)

        if response.status_code == 201:
            st.success(response)
        else:
            st.error("Request failed. Please check the URL and try again.")

    tabs = sac.tabs(
        [
            dict(label="Chat", icon="chat-fill"),
            dict(label="Docs", icon="file-post"),
            dict(label="Graph", icon="bezier"),
            dict(label="Structure", icon="strava"),
            dict(label="Status", icon="check-circle-fill"),
        ],
        align="center",
        return_index=True,
    )
    if tabs == 0:
        for selected_item in selected_items:
            selected_data = next(
                (item for item in data if item["title"] == selected_item), None
            )
            print(selected_data)

            reset = sac.buttons(
                ["Reset"],
                label=None,
                index=0,
                format_func="title",
                align="end",
                position="bottom",
                size="default",
                direction="horizontal",
                shape="default",
                compact=False,
                return_index=True,
            )

            if reset:
                st.session_state.reset
                st.session_state.messages = []
                st.session_state.session_id = str(uuid4())

            if "messages" not in st.session_state:
                st.session_state.messages = []

            if f"Hello, ask me anything about {selected_data['title']}!" not in [
                msg["content"]
                for msg in st.session_state.messages
                if msg["role"] == "assistant"
            ]:
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": f"Hello, ask me anything about {selected_data['title']}!",
                    }
                )

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            if prompt := st.chat_input("Ask me!"):
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

    if tabs == 1:
        for selected_item in selected_items:
            selected_data = next(
                (item for item in data if item["title"] == selected_item), None
            )
            data = fetch_data_from_api(
                f"{setting.API_ENDPOINT}/api/data/summary?title={selected_data['title']}"
            )
            st.markdown(data)

    if tabs == 2:
        for selected_item in selected_items:
            selected_data = next(
                (item for item in data if item["title"] == selected_item), None
            )
            data = fetch_data_from_api(
                f"{setting.API_ENDPOINT}/api/data/graph?title={selected_data['title']}&formatted=true"
            )
            nodes = []
            edges = []

            for graph_elem in data:
                node_id = graph_elem["name"]
                size = 40 * (1 + graph_elem["size_percentage"])

                if node_id and node_id.lower() not in [n.id.lower() for n in nodes]:
                    nodes.append(Node(id=node_id, label=node_id, size=size))

                for subject_related in graph_elem["subject_related"]:
                    if subject_related and subject_related.lower() not in [
                        n.id.lower() for n in nodes
                    ]:
                        nodes.append(
                            Node(id=subject_related, label=subject_related, size=size)
                        )
                        edges.append(Edge(source=node_id, target=subject_related))

            config = Config(
                width=750,
                height=700,
                directed=False,
                physics=True,
                hierarchical=False,
            )

            try:
                agraph(nodes=nodes, edges=edges, config=config)
            except Exception as exc:
                st.error(f"Graph rendering error: {exc}")

    if tabs == 4:
        step_label = ["Cloning", "Embedding", "Summarizing", "Graph", "Done"]
        for selected_item in selected_items:
            selected_data = next(
                (item for item in data if item["title"] == selected_item), None
            )
        step_status = 0
        if selected_data["status"] == "started":
            step_status = 0
        if selected_data["status"] == "embedding":
            step_status = 1
        if selected_data["status"] == "summary":
            step_status = 2
        if selected_data["status"] == "grpah":
            step_status = 3
        if selected_data["status"] == "done":
            step_status = 4
        st.write("Relax! ")
        st.write(f"Process is {step_label[step_status].lower()}.")
        sac.steps(
            step_label,
            index=step_status,
            format_func="title",
            placement="vertical",
            size="default",
            direction="horizontal",
            type="default",
            dot=False,
            return_index=True,
        )
