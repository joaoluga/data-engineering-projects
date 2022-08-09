module "metabase_ecr" {
  source = "../../modules/ecr"
  ecr_name = "${var.project_name}-metabase"
  tags = local.default_tags
}