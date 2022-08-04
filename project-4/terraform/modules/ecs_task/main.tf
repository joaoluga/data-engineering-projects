resource "aws_ecs_task_definition" "task" {
  family = var.task_name
  network_mode = "awsvpc"
  execution_role_arn = var.execution_role_arn
  task_role_arn = var.task_role_arn
  requires_compatibilities = [var.launch_type]
  cpu = var.cpu
  memory = var.memory
  container_definitions = var.container_definitions

  tags = merge(var.tags, {Resource = "ecs-task-definition-${var.task_name}"})
}

resource "aws_ecs_service" "ecs_service" {
  name = var.ecs_service_name
  cluster = var.ecs_cluster_id
  task_definition = aws_ecs_task_definition.task.arn
  desired_count = var.desired_count
  launch_type = var.launch_type
  deployment_maximum_percent = var.deployment_maximum_percent
  deployment_minimum_healthy_percent = var.deployment_minimum_percent
  health_check_grace_period_seconds = var.health_check_grace_period_seconds

  network_configuration {
    security_groups = var.ecs_service_security_groups
    subnets = var.ecs_service_subnets
    assign_public_ip = true
  }

  dynamic load_balancer {
    for_each = var.create_with_load_balancer == true? [1] : []
    content {
      target_group_arn = var.lb_target_group_arn
      container_name   = var.lb_container_name
      container_port   = var.lb_container_port
    }
  }

  tags = merge(var.tags, {Resource = "ecs_service-${var.ecs_service_name}"})
}