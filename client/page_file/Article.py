import requests
import streamlit as st
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


st.title("Article Data")

# Sidebar
data = fetch_data_from_api(f"{setting.API_ENDPOINT}/api/data/?source=web")
selected_items = st.sidebar.multiselect(
    "Select a data",
    options=[item["title"] for item in data],
    default=None,
    format_func=lambda item: item,
)

# Display selected data
for selected_item in selected_items:
    selected_data = next(
        (item for item in data if item["title"] == selected_item), None
    )
    if selected_data:
        st.write("Selected Item Details:")
        st.write(f"Title: {selected_data['title']}")
        st.write(f"Type: {selected_data['type']}")
        st.write(f"Source: {selected_data['source']}")
        st.write(f"Status: {selected_data['status']}")

        MIN_SIZE = 40
        MAX_SIZE = 15

        data = fetch_data_from_api(
            f"http://localhost:8000/api/data/graph?title={selected_data['title']}&formatted=true"
        )

        nodes = []
        edges = []

        for graph_elem in data:
            if graph_elem["name"] != "":
                if graph_elem["name"].lower() not in [n.id.lower() for n in nodes]:
                    nodes.append(
                        Node(
                            id=graph_elem["name"],
                            label=graph_elem["name"],
                            size=MAX_SIZE * (1 + graph_elem["size_percentage"]),
                        )
                    )

            for subject_related in graph_elem["subject_related"]:
                if subject_related != "":
                    if subject_related.lower() not in [n.id.lower() for n in nodes]:
                        try:
                            nodes.append(
                                Node(
                                    id=subject_related,
                                    label=subject_related,
                                    size=MAX_SIZE * (1 + graph_elem["size_percentage"]),
                                )
                            )
                        except:
                            pass

                        try:
                            edges.append(
                                Edge(
                                    source=graph_elem["name"],
                                    # label=graph_elem["name"],
                                    target=subject_related,
                                    # **kwargs
                                )
                            )
                        except:
                            pass

        config = Config(
            width=750,
            height=950,
            directed=False,
            physics=True,
            hierarchical=False,
            # **kwargs
        )

        try:
            return_value = agraph(nodes=nodes, edges=edges, config=config)
        except Exception as exc:
            print(f"Error: {exc}")
        st.write(return_value)
