resource "aws_security_group" "ecs_sg" {
  vpc_id      = data.aws_vpc.main.id

    ingress {
      from_port       = 0
      to_port         = 0
      protocol        = "-1"
      cidr_blocks     = ["0.0.0.0/0"]
      security_groups = [aws_security_group.application_load_balancer.id]
    }

    egress {
      from_port       = 0
      to_port         = 0
      protocol        = "-1"
      cidr_blocks     = ["0.0.0.0/0"]
    }

  tags = merge(local.default_tags, {Resource = "security_group-ecs"}, {Application = "ECS"})
}

resource "aws_security_group" "rds_sg" {
  vpc_id      = data.aws_vpc.main.id

  ingress {
    protocol        = "tcp"
    from_port       = 5432
    to_port         = 5432
    cidr_blocks     = ["0.0.0.0/0"]
    security_groups = [aws_security_group.ecs_sg.id]
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
  }

  tags = merge(local.default_tags, {Resource = "security_group-rds"}, {Application = "RDS"})
}


resource "aws_security_group" "application_load_balancer" {
  vpc_id = data.aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
  }
  tags = merge(local.default_tags, {Resource = "security_group-alb"}, {Application = "ALB"})
}