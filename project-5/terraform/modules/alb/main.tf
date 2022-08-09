resource "aws_alb" "alb" {
  name            = var.alb_name
  subnets         = var.subnets_ids
  security_groups = var.security_groups
  tags            = merge(var.tags, {Resource = "alb-${var.alb_name}"})
}

resource "aws_alb_target_group" "target_group" {
  name        = "${var.alb_name}-alb-target-group"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = var.vpc_id
  target_type = var.target_type

  health_check {
    interval = var.health_check_interval
    port = 80
    protocol = "HTTP"
    path = var.health_check_path
    timeout = var.health_check_timeout
    healthy_threshold = var.health_check_healthy_threshold
    unhealthy_threshold = var.health_check_unhealthy_threshold
  }
  tags = merge(var.tags, {Resource = "alb_target_group-${var.alb_name}"})
}

resource "aws_alb_listener" "listener_http" {
  load_balancer_arn = aws_alb.alb.arn
  port = "80"
  protocol = "HTTP"

  default_action {
    target_group_arn = aws_alb_target_group.target_group.arn
    type = "forward"
  }

  tags = merge(var.tags, {Resource = "listener-http-${var.alb_name}"})
}