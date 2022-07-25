from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.onprem.database import Postgresql
from diagrams.onprem.container import Docker
from diagrams.onprem.analytics import Dbt
from diagrams.onprem.workflow import Airflow
from diagrams.programming.language import Python


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
    "Project 3 - ETL with Apache Airflow and DBT",
    outformat="png",
    show=False,
    filename="architecture",
    # ("TB", "BT", "LR", "RL")
    direction="LR",
    node_attr=node_attrs,
    curvestyle="ortho",
):

    with Cluster(label="Docker - Container Area", graph_attr=graph_attrs):
        docker = Docker("docker-compose")
        jupyter_lab = Custom("Jupyter Lab", "./source_images/jupyter.png")
        jupyter_api = Custom("Jupyter API", "./source_images/jupyter.png")
        pg_analytics = Postgresql("Analytics")
        pg_airflow = Postgresql("Airflow Backend")
        airflow = Airflow("Airflow")
        dbt_docs_service = Dbt("dbt_docs")

        # Docker Containers
        (
            docker
            >> Edge(color="darkblue")
            >> [
                jupyter_lab,
                jupyter_api,
                pg_analytics,
                airflow,
                dbt_docs_service,
                pg_airflow,
            ]
        )

        # Relation Between containers
        pg_airflow >> Edge(color="dark") >> airflow
        # airflow >> Edge(color="dark") >> pg_airflow
        # jupyter_api >> Edge(color="darkred", style="dashed") >> jupyter_lab
        with Cluster("ETL area", graph_attr=graph_attrs):

            with Cluster("Star Schema DAG", graph_attr=graph_attrs):
                airflow_dag = Airflow("star_schema.py")
                airflow >> Edge(color="purple", style="dashed") >> airflow_dag
                dbt_doc_gen = Dbt("DBT Generate Docs")
                python = Python("Call Jupyter API")
                dbt_run = Dbt("DBT Run")
                airflow_dag >> Edge(color="darkred", style="dashed") >> python
                python >> jupyter_api
                (
                    python
                    >> dbt_run
                    >> dbt_doc_gen
                    << Edge(color="purple", style="dashed")
                    << dbt_docs_service
                )

            with Cluster("Analytics Database"):
                # Tables of Pg Analytics
                trusted = Custom("Trusted", "./source_images/tables.png")
                refined = Custom("Refined", "./source_images/tables.png")
                pg_analytics >> Edge(color="purple", style="dashed") >> trusted

            with Cluster("Jupyter Lab Area", graph_attr=graph_attrs):
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
                etl = Custom("ETL Worlflow", "./source_images/notebook.png")

                data_sources >> Edge(color="darkorange", style="dashed") >> etl
                (
                    jupyter_api
                    >> Edge(color="purple", style="dashed")
                    >> etl
                    >> Edge(color="darkorange", style="dashed")
                    >> trusted
                )
                dbt_run << trusted
                dbt_run >> refined
                jupyter_lab >> Edge(color="purple", style="dashed") >> etl

                # dbt_doc_gen = Dbt("DBT Generate Docs")
                # dbt_run = Dbt("DBT Run")
                # data_sources >> Edge(color="darkorange", style="dashed") >> etl >> Edge(color="dark") >> trusted
                # airflow_dag >> Edge(color="darkred", style="dashed") >> [jupyter_api, dbt_run, dbt_doc_gen]
                # airflow >> airflow_dag

            with Cluster("Data Viz. Area"):

                dataviz = Custom("Seaborn\nDasbharods", "./source_images/notebook.png")
                refined >> Edge(color="darkorange", style="dashed") >> dataviz
                jupyter_lab >> Edge(color="purple", style="dashed") >> dataviz
