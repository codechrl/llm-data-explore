from uuid import uuid4

import streamlit as st
import streamlit_antd_components as sac
from page_file import (
    files_article,
    files_youtube,
    repository_github_data,
    repository_github_overview,
)
from streamlit_agraph import Config, Edge, Node, agraph

st.set_page_config(page_title="EXTORY", layout="wide")

query_params = st.experimental_get_query_params()

if "new" not in st.session_state:
    st.session_state["new"] = True
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid4())
# sac.divider()
# tabs = sac.tabs(["Chat", "Overview", "Data"], align="center", return_index=True)

# if tabs == 1:
#     st.write(tabs)

with st.sidebar:
    menu_index = sac.menu(
        [
            sac.MenuItem(
                "home",
                icon="house-fill",
            ),
            sac.MenuItem(
                "Repository",
                icon="journal-code",
                children=[
                    sac.MenuItem(
                        "GitHub",
                        icon="github",
                        children=[
                            sac.MenuItem("Overview", icon="collection-fill"),
                            sac.MenuItem("data", icon="file-earmark-code-fill"),
                        ],
                    ),
                    sac.MenuItem(
                        "Gitlab",
                        icon="git",
                        # disabled=True,
                        tag=sac.Tag("On Development", color="yellow", bordered=False),
                        children=[
                            sac.MenuItem(
                                "Overview", icon="collection-fill", disabled=True
                            ),
                            sac.MenuItem(
                                "data", icon="file-earmark-code-fill", disabled=True
                            ),
                        ],
                    ),
                ],
            ),
            sac.MenuItem(
                "Files",
                icon="file-earmark-fill",
                children=[
                    sac.MenuItem(
                        "Overview",
                        icon="collection-fill",
                        tag=sac.Tag("On Development", color="yellow", bordered=False),
                        disabled=True,
                    ),
                    sac.MenuItem(
                        "youtube",
                        icon="file-play-fill",
                        tag=sac.Tag("New", color="green", bordered=False),
                    ),
                    sac.MenuItem("Article", icon="browser-chrome"),
                ],
            ),
            sac.MenuItem(type="divider"),
            # sac.MenuItem(
            #     "Extory",
            #     type="group",
            #     children=[
            #         sac.MenuItem(
            #             r"Xquisite AI",
            #             icon="heart",
            #             href="https://ant.design/components/menu#menu",
            #         ),
            #         sac.MenuItem(
            #             "2023, Extory All Right Reserved",
            #             icon="bootstrap",
            #             href="https://icons.getbootstrap.com/",
            #         ),
            #     ],
            # ),
        ],
        index=0,
        format_func="title",
        size="middle",
        indent=24,
        open_index=None,
        open_all=True,
        return_index=True,
    )


# st.write(menu_index)
# st.write(query_params)
title = None
try:
    title = query_params["title"][0]
    if query_params["title"][0]:
        menu_index = 4
        if "new" not in st.session_state:
            st.session_state["new"] = False

        st.session_state["new"] = False
        repository_github_data.page(
            query_params["title"][0],
            query_params["question"][0],
        )
    else:
        st.session_state["new"] = True
except:
    if "new" not in st.session_state:
        st.session_state["new"] = True


if menu_index == 0:
    st.subheader("Hello :wave:")
    st.title("Welcome to Extory!")
    # nodes = []
    # edges = []

    # data = [
    #     {
    #         "name": "EXTORY",
    #         "subject_related": ["Data", "Repository", "Files", "Story", "AI", "Chat"],
    #     },
    #     {
    #         "name": "Files",
    #         "subject_related": ["Video", "Web", "Article", "Text", "Youtube"],
    #     },
    #     {
    #         "name": "Repository",
    #         "subject_related": ["GitHub", "Git", "Gitlab", "BitBucket", "Code"],
    #     },
    # ]

    # for graph_elem in data:
    #     node_id = graph_elem["name"]
    #     # size = 40 * (1 + graph_elem["size_percentage"])
    #     size = 40

    #     if node_id and node_id.lower() not in [n.id.lower() for n in nodes]:
    #         nodes.append(
    #             Node(
    #                 id=node_id,
    #                 label=node_id,
    #                 size=(size if node_id == "Extory" else 100),
    #                 color="#FF0000",
    #             )
    #         )

    #     for subject_related in graph_elem["subject_related"]:
    #         if subject_related and subject_related.lower() not in [
    #             n.id.lower() for n in nodes
    #         ]:
    #             nodes.append(
    #                 Node(
    #                     id=subject_related,
    #                     label=subject_related,
    #                     size=size,
    #                     title=subject_related,
    #                 )
    #             )
    #             edges.append(
    #                 Edge(source=node_id, target=subject_related, color="#FFFFFF")
    #             )

    # config = Config(
    #     width=1200,
    #     height=700,
    #     directed=False,
    #     physics=True,
    #     hierarchical=False,
    #     node={
    #         "labelProperty": "label",
    #         "style": {"color": "#FFFFFF"},
    #         "renderLabel": True,
    #     },
    #     nodeHighlightBehavior=True,
    #     color="#FFFFFF",
    #     strokeColor="#FFFFFF",
    # )

    # try:
    #     agraph(nodes=nodes, edges=edges, config=config)
    # except Exception as exc:
    #     st.error(f"Graph rendering error: {exc}")

if menu_index == 3:
    repository_github_overview.page()

if menu_index == 4 and not title:
    st.session_state.new = True
    repository_github_data.page()

if menu_index == 7:
    files_youtube.page()

if menu_index == 8:
    files_article.page()
