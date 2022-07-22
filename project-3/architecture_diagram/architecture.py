from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.onprem.database import Postgresql
from diagrams.onprem.container import Docker


graph_attrs = {
    "shape": "box",
    "style": "rounded",
    "labeljust": "l",
    "pencolor": "#d69a96",
    "fontname": "Sans-Serif",
    "fontsize": "18",
    "center": "true",
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
    "center": "true",
}


with Diagram(
    "Project 2 - ETL with Python and SQL",
    outformat="png",
    show=False,
    filename="architecture",
    direction="LR",
    # node_attr=node_attrs,
    curvestyle="ortho",
):

    with Cluster("Docker Area", graph_attr=graph_attrs):
        docker = Docker("docker-compose")
        jupyter = Custom("Jupyter", "./source_images/jupyter.png")
        pg = Postgresql("Postgres")
        docker >> jupyter
        docker >> pg

        with Cluster("Data Sources", graph_attr=graph_attrs):
            csv = Custom(
                "Ranking de\ninstituições\npor índice de\nreclamações\n",
                "./source_images/csv.png",
            )
            api = Custom(
                "Tarifas bancarias\npor segmento e\npor instituição",
                "./source_images/api.png",
            )
            data_sources = [api, csv]

        with Cluster("ETL Area", graph_attr=graph_attrs):
            etl = Custom("ETL Worlflow", "./source_images/notebook.png")
            tables = Custom("Tables", "./source_images/tables.png")
            (
                data_sources
                >> Edge(color="darkorange", style="dashed")
                >> etl
                >> Edge(color="dark")
                >> tables
            )
            etl << Edge(color="dark") << tables
            jupyter >> etl
            pg >> tables

        with Cluster("Data Viz. Area", graph_attr=graph_attrs):
            dataviz = Custom("Seaborn\nDasbharods", "./source_images/notebook.png")
            tables >> Edge(color="darkorange", style="dashed") >> dataviz
            jupyter >> dataviz
