locals {
  default_tags = merge(var.tags, {Application = "Airflow"})

  ### ECS SERVICES / TASK DEFAULT VALUES
  ecr_image          = "${module.airflow_ecr.repository_url}:latest"
  port               = 8080
  listener_port      = 80
  logging_bucket     = "s3://${aws_s3_bucket.airflow_logs.id}"
  awslogs_group      = "ecs/${var.project_name}"

}