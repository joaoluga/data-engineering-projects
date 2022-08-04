resource "aws_ecs_cluster" "ecs_cluster" {
  name = var.ecs_cluster_name
  tags  = merge(var.tags, {Resource = "ecs_cluster-${var.ecs_cluster_name}"})
}

resource "aws_cloudwatch_log_group" "log_group" {
  name = "ecs/${var.ecs_cluster_name}"
  retention_in_days = var.retention_in_days
  tags = merge(var.tags, {Resource = "log_group-ecs/${var.ecs_cluster_name}"})
}