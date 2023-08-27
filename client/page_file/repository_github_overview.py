from uuid import uuid4

import requests
import streamlit as st
import streamlit_antd_components as sac
from setting import setting
from streamlit_agraph import Config, Edge, Node, agraph
from util import fetch_data_from_api


def page(new=False):
    st.subheader("Repository Github Overview!")
    st.session_state.session_id = str(uuid4())
    url = st.sidebar.text_input("Input repository clone URL")
    submit_button = st.sidebar.button("Submit")
    if submit_button:
        if url:
            url = f"{setting.API_ENDPOINT}/api/engine/repository?background=true&url={url}"
            response = requests.post(url)
            if response.status_code == 201:
                st.success("Request successful")
                # page()
            else:
                st.error("Request failed. Please check the URL and try again.")

    # data = fetch_data_from_api(f"{setting.API_ENDPOINT}/api/data/?type=repository")
    # selected_items = st.sidebar.multiselect(
    #     "Select a repository",
    #     options=[item["title"] for item in data],
    #     default=data[0]["title"],
    #     format_func=lambda item: item,
    # )

    tabs = sac.tabs(
        [
            dict(label="Chat", icon="chat-fill"),
            dict(label="Docs", icon="file-post"),
            dict(label="Graph", icon="bezier"),
            # dict(label="Structure", icon="strava"),
            dict(label="Status", icon="check-circle-fill"),
        ],
        align="center",
        return_index=True,
    )
    data = [{"title": "overview_repository"}]
    # selected_item = "overview_repository"
    if tabs == 0:
        selected_data = {
            "title": "overview_repository",
            "type": "repository",
            "source": "github",
            "status": "done",
        }

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
                        "title": "overview_repository",
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
        selected_data = {
            "title": "overview_repository",
            "type": "repository",
            "source": "github",
            "status": "done",
        }
        data = fetch_data_from_api(
            f"{setting.API_ENDPOINT}/api/data/docs?title={selected_data['title']}"
        )
        st.markdown(data)

    if tabs == 2:
        selected_data = {
            "title": "overview_repository",
            "type": "repository",
            "source": "github",
            "status": "done",
        }
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
        reset = sac.buttons(
            ["Update Repo"],
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
        step_label = ["Cloning", "Embedding", "Summarizing", "Graph", "Done"]

        selected_data = {
            "title": "overview_repository",
            "type": "repository",
            "source": "github",
            "status": "done",
        }
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
