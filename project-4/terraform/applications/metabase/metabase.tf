module "alb_metabase" {
  source = "../../modules/alb"
  alb_name = "metabase-${var.environment}"
  subnets_ids = var.subnet_ids
  security_groups = var.alb_security_groups
  health_check_interval = 70
  health_check_path = "/"
  health_check_timeout = 40
  health_check_healthy_threshold = 5
  health_check_unhealthy_threshold = 3
  vpc_id = var.vpc_id
  tags = local.default_tags
}

module "ecs_task_metabase" {
  source = "../../modules/ecs_task"
  ecs_service_name = "metabase-service-${var.environment}"
  ecs_cluster_id = var.ecs_cluster_id
  deployment_maximum_percent = 200
  deployment_minimum_percent = 100
  health_check_grace_period_seconds = 6
  desired_count = 2
  ecs_service_security_groups = var.ecs_security_groups
  ecs_service_subnets = var.subnet_ids
  create_with_load_balancer = true
  lb_target_group_arn = module.alb_metabase.target_group_arn
  lb_container_name = "metabase"
  lb_container_port = local.port
  task_name = "metabase_task"
  execution_role_arn = var.execution_role_arn
  task_role_arn = var.execution_role_arn
  cpu = "1024"
  memory = "2048"
  container_definitions = templatefile("${path.module}/metabase_task.json", {
    db_uri             = module.metabase_rds.jdbc_conn
    awslogs_group      = local.awslogs_group
    awslogs_region     = var.region
    port               = local.port
  })
  tags = local.default_tags
}