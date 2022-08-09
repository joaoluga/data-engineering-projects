module "airflow_ecr" {
  source = "../../modules/ecr"
  ecr_name = "${var.project_name}-airflow"
  tags = local.default_tags
}