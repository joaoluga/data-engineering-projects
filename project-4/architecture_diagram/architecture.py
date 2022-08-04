from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.workflow import Airflow
from diagrams.aws.analytics import EMRCluster
from diagrams.aws.database import RDSPostgresqlInstance
from diagrams.aws.network import ElbApplicationLoadBalancer
from diagrams.aws.storage import SimpleStorageServiceS3
from diagrams.aws.compute import Fargate
from diagrams.aws.compute import ElasticContainerService


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
    "Project 4 - ETL with EMR",
    outformat="png",
    show=False,
    filename="architecture",
    # ("TB", "BT", "LR", "RL")
    direction="TB",
    node_attr=node_attrs,
    curvestyle="ortho",
):

    with Cluster(label="AWS - Area", graph_attr=graph_attrs):
        emr = EMRCluster('EMR-Spot')
        rds_analytics = RDSPostgresqlInstance('rds_analytics')
        rds_airflow = RDSPostgresqlInstance('rds_airflow')
        rds_metabase = RDSPostgresqlInstance('rds_metabase')
        alb_airflow = ElbApplicationLoadBalancer('alb_airflow')
        alb_metabase = ElbApplicationLoadBalancer('alb_metabase')
        data_lake = SimpleStorageServiceS3('s3_data_lake')
        emr_s3 = SimpleStorageServiceS3('s3_emr')

        with Cluster(label="ECS Cluster", graph_attr=graph_attrs):
            dag = Airflow('star_schema_dag')
            ecs = ElasticContainerService()
            airflow_webserver = Fargate("airflow_webserver")
            airflow_scheduler = Fargate("airflow_scheduler")
            metabase = Fargate("metabase")

            #airflow_webserver
            ecs >> airflow_webserver << Edge(color="purple", style='dashed') << alb_airflow
            airflow_webserver >> dag

            #airflow_scheduler
            ecs >> airflow_scheduler >> dag >> Edge(color="darkorange", style='dashed') >> emr >> Edge(color="darkred") >> data_lake
            emr >> Edge(color="darkred") >> rds_analytics
            emr << Edge(color="darkred") << emr_s3
            airflow_scheduler >> Edge(color="darkorange", style='dashed') >> rds_airflow

            # metabase
            ecs >> metabase
            metabase << Edge(color="purple", style='dashed') << alb_metabase
            metabase >> Edge(color="darkorange", style='dashed') >> rds_metabase
            metabase << Edge(color="purple", style='dashed') << rds_analytics






