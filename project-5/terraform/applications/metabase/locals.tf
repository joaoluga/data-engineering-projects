locals {
  default_tags = merge(var.tags, {Application = "Metabase"})

  ### ECS SERVICES / TASK DEFAULT VALUES
  port               = 3000
  awslogs_group      = "ecs/${var.project_name}"

}