module "ecs_cluster" {
  source = "./modules/ecs"
  ecs_cluster_name  = var.project_name
  retention_in_days = 1
  tags = merge(local.default_tags, {Resource = "ecs_cluster-${var.project_name}"}, {Application = "Airflow"})
}