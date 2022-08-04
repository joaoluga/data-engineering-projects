module "airflow_ecr" {
  source = "../../modules/ecr"
  ecr_name = var.project_name
  tags = local.default_tags
}