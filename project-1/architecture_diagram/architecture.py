from diagrams import Diagram, Cluster, Edge, Node
from diagrams.custom import Custom
from diagrams.onprem.database import Postgresql
from diagrams.onprem.analytics import Metabase


graph_attrs = {
    "shape": "box",
    "style": "rounded",
    "labeljust": "l",
    "pencolor": "#d69a96",
    "fontname": "Sans-Serif",
    "fontsize": "18",
    "center": 'true',
    "fixedsize": "true",
}

node_attrs = {
    "shape": "box",
    "style": "rounded",
    "fixedsize": "true",
    "width": "1.0",
    "height": "1.6",
    "labelloc": "b",
    "landscape": "true",
    "imagescale": "true",
    "fontname": "Sans-Serif",
    "fontsize": "12",
    "fontcolor": "#2D3436",
    "center": 'true',
}


with Diagram(
        "Project 1 - ETL with Drag-and-Drop Orchestration Tool", outformat="png", show=False,
        filename="architecture", direction='LR',
        node_attr=node_attrs,
        curvestyle="ortho"):

    with Cluster("Data Sources", graph_attr=graph_attrs):
        csv = Custom("Ranking de\ninstituições\npor índice de\nreclamações\n", "./source_images/csv.png")
        api = Custom("Tarifas bancarias\npor segmento e\npor instituição", "./source_images/api.png")
        data_sources = [
            api,
            csv
        ]

    with Cluster("ETL Area", graph_attr=graph_attrs):
        hop = Custom("Apache Hop", "./source_images/hop.png")
        pg = Postgresql("Postgres")
        data_sources >> Edge(color="darkorange", style="dashed") >> hop >> Edge(color="dark") >> pg
        hop << Edge(color="dark") << pg

    with Cluster("Data Viz. Area", graph_attr=graph_attrs):
        metabase = Metabase("Metabase")
        pg >> Edge(color="darkorange", style="dashed") >> metabase
