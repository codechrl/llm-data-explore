import requests
import streamlit as st
from setting import setting
from streamlit_agraph import Config, Edge, Node, agraph

# Set page configuration
st.set_page_config(layout="wide")


# Function to fetch data from the API
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


# Sidebar
url = st.sidebar.text_input("Input repository clone URL")
submit_button = st.sidebar.button("Submit")

# Fetch data from the API and allow user selection
data = fetch_data_from_api(f"{setting.API_ENDPOINT}/api/data/?type=repository")
selected_items = st.sidebar.multiselect(
    "Select a repository",
    options=[item["title"] for item in data],
    default=None,
    format_func=lambda item: item,
)

# Handle user input
if submit_button:
    if url:
        url = f"{setting.API_ENDPOINT}/api/engine/repository?background=true&url={url}"
        response = requests.post(url)
        if response.status_code == 201:
            st.success("Request successful")
        else:
            st.error("Request failed. Please check the URL and try again.")

# Display selected data
for selected_item in selected_items:
    selected_data = next(
        (item for item in data if item["title"] == selected_item), None
    )
    if selected_data:
        st.title(selected_data["title"])
        # st.write(f"**Title:** {selected_data['title']}")
        st.write(f"**Type:** {selected_data['type']}")
        st.write(f"**Source:** {selected_data['source']}")
        st.write(f"**Status:** {selected_data['status']}")

        MIN_SIZE = 40
        MAX_SIZE = 15

        data = fetch_data_from_api(
            f"{setting.API_ENDPOINT}/api/data/graph?title={selected_data['title']}&formatted=true"
        )
        docs = fetch_data_from_api(
            f"{setting.API_ENDPOINT}/api/data/docs?title={selected_data['title']}"
        )
        summary = fetch_data_from_api(
            f"{setting.API_ENDPOINT}/api/data/summary?title={selected_data['title']}"
        )

        try:
            with st.expander("Summary"):
                st.write(summary)
        except:
            pass

        try:
            with st.expander("Docs"):
                st.markdown(docs)
        except:
            pass

        try:
            with st.expander("Graph"):
                nodes = []
                edges = []

                for graph_elem in data:
                    node_id = graph_elem["name"]
                    size = MAX_SIZE * (1 + graph_elem["size_percentage"])

                    if node_id and node_id.lower() not in [n.id.lower() for n in nodes]:
                        nodes.append(Node(id=node_id, label=node_id, size=size))

                    for subject_related in graph_elem["subject_related"]:
                        if subject_related and subject_related.lower() not in [
                            n.id.lower() for n in nodes
                        ]:
                            nodes.append(
                                Node(
                                    id=subject_related, label=subject_related, size=size
                                )
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
        except:
            pass

    st.markdown(f"[*Click here to chat with this repo!*]({url})")
