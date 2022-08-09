resource "random_password" "pwd" {
  length           = 24
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "aws_ssm_parameter" "admin_pwd" {
  name        = "/airflow/admin_pwd"
  description = "admin pwd"
  type        = "SecureString"
  value       = random_password.pwd.result

  tags = merge(var.tags, {Resource = "/airflow/admin_pwd"})
}

module "alb_webserver" {
  source = "../../modules/alb"
  alb_name = "webserver-${var.environment}"
  subnets_ids = var.subnet_ids
  security_groups = var.alb_security_groups
  health_check_interval = 70
  health_check_path = "/health"
  health_check_timeout = 40
  health_check_healthy_threshold = 5
  health_check_unhealthy_threshold = 3
  vpc_id = var.vpc_id
  tags = local.default_tags
}

module "ecs_task_webserver" {
  source = "../../modules/ecs_task"
  ecs_service_name = "webserver-service-${var.environment}"
  ecs_cluster_id = var.ecs_cluster_id
  deployment_maximum_percent = 200
  deployment_minimum_percent = 100
  desired_count = 2
  health_check_grace_period_seconds = 60
  ecs_service_security_groups = var.ecs_security_groups
  ecs_service_subnets = var.subnet_ids
  create_with_load_balancer = true
  lb_target_group_arn = module.alb_webserver.target_group_arn
  lb_container_name = "airflow_webserver"
  lb_container_port = local.port
  task_name = "airflow_webserver"
  execution_role_arn = var.execution_role_arn
  task_role_arn = var.execution_role_arn
  cpu = "1024"
  memory = "2048"
  container_definitions = templatefile("${path.module}/airflow_webserver_task.json", {
    command            = "webserver"
    ecr_image          = local.ecr_image,
    port               = local.port
    sql_alchemy_conn   = module.airflow_rds.sqlalchemy_conn
    logging_bucket     = local.logging_bucket
    awslogs_group      = local.awslogs_group,
    awslogs_region     = var.region
    admin_pwd          = aws_ssm_parameter.admin_pwd.value
  })
  tags = local.default_tags
}