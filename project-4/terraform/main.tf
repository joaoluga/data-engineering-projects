module "airflow_services" {
  source = "./applications/airflow"
  project_name = var.project_name
  environment = var.environment
  ecs_cluster_id = module.ecs_cluster.ecs_cluster_id
  alb_security_groups = [aws_security_group.application_load_balancer.id]
  rds_security_groups = [aws_security_group.rds_sg.id]
  ecs_security_groups = [aws_security_group.ecs_sg.id]
  subnet_ids = data.aws_subnets.subnets.ids
  execution_role_arn = data.aws_iam_role.lab_role.arn
  emr_bucket_name = aws_s3_bucket.emr.id
  vpc_id = data.aws_vpc.main.id
  tags = local.default_tags
}

module "metabase_service" {
  source = "./applications/metabase"
  project_name = var.project_name
  environment = var.environment
  ecs_cluster_id = module.ecs_cluster.ecs_cluster_id
  alb_security_groups = [aws_security_group.application_load_balancer.id]
  rds_security_groups = [aws_security_group.rds_sg.id]
  ecs_security_groups = [aws_security_group.ecs_sg.id]
  subnet_ids = data.aws_subnets.subnets.ids
  execution_role_arn = data.aws_iam_role.lab_role.arn
  vpc_id = data.aws_vpc.main.id
  tags = local.default_tags
}