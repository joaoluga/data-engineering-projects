from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.workflow import Airflow
from diagrams.aws.analytics import Glue, GlueCrawlers, GlueDataCatalog, Athena
from diagrams.aws.database import RDSPostgresqlInstance
from diagrams.aws.network import ElbApplicationLoadBalancer
from diagrams.aws.storage import SimpleStorageServiceS3
from diagrams.aws.compute import Fargate

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
    "Project 5 - ETL with Serverless Services",
    outformat="png",
    show=False,
    filename="architecture",
    # ("TB", "BT", "LR", "RL")
    direction="LR",
    node_attr=node_attrs,
    curvestyle="ortho",
):

    with Cluster(label="AWS - Area", graph_attr=graph_attrs):

        with Cluster(label="ECS Area", graph_attr=graph_attrs):
            with Cluster(label="Metabase Application", graph_attr=graph_attrs):
                metabase = Fargate("metabase")
                alb_metabase = ElbApplicationLoadBalancer('alb_metabase')
                rds_metabase = RDSPostgresqlInstance('rds_metabase')

            with Cluster(label="Apache Airflow Application", graph_attr=graph_attrs):
                dag = Airflow('star_schema_dag')
                airflow_webserver = Fargate("airflow_webserver")
                airflow_scheduler = Fargate("airflow_scheduler")
                rds_airflow = RDSPostgresqlInstance('rds_airflow')
                alb_airflow = ElbApplicationLoadBalancer('alb_airflow')

        with Cluster(label="Processing Area", graph_attr=graph_attrs):
            athena = Athena('Athena')
            glue = Glue('Glue Jobs - 3.0')
            glue_crawler = GlueCrawlers("Trusted\nand Refined\nCrawlers")
            glue_catalog = GlueDataCatalog("Trusted\nand Refined\nCatalogs")
            data_lake = SimpleStorageServiceS3('s3_data_lake')
            glue_s3 = SimpleStorageServiceS3('s3_glue')

        #airflow_webserver
        airflow_webserver << alb_airflow
        airflow_webserver << rds_airflow

        #airflow_scheduler
        airflow_scheduler >> dag >> Edge(color="darkorange", style='dashed') >> glue >> data_lake
        data_lake << glue_crawler >> glue_catalog >> athena
        glue << glue_s3
        airflow_scheduler >> rds_airflow

        # metabase
        metabase << alb_metabase
        metabase >> rds_metabase
        metabase << Edge(color="darkorange", style="dashed") << athena




