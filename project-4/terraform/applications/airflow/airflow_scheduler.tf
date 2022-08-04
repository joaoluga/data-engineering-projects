module "ecs_task_scheduler" {
  source = "../../modules/ecs_task"
  ecs_service_name = "scheduler-service-${var.environment}"
  ecs_cluster_id = var.ecs_cluster_id
  ecs_service_security_groups = var.ecs_security_groups
  ecs_service_subnets = var.subnet_ids
  task_name = "airflow_scheduler"
  execution_role_arn = var.execution_role_arn
  task_role_arn = var.execution_role_arn
  cpu = "1024"
  memory = "2048"
  container_definitions = templatefile("${path.module}/airflow_scheduler_task.json", {
    command            = "scheduler"
    ecr_image          = local.ecr_image
    port               = local.port
    sql_alchemy_conn   = module.airflow_rds.sqlalchemy_conn
    logging_bucket     = local.logging_bucket
    awslogs_group      = local.awslogs_group
    awslogs_region     = var.region
    emr_bucket_name    = var.emr_bucket_name
  })
  tags = local.default_tags
}