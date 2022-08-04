variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable ecs_cluster_id {
  type = string
}

variable ecs_security_groups {
  type = list(string)
}

variable subnet_ids {
  type = list(string)
}

variable execution_role_arn {
  type = string
}

variable alb_security_groups {
  type = list(string)
}

variable rds_security_groups {
  type = list(string)
}

variable vpc_id {
  type = string
}

variable tags {
  type = map(string)
}

variable "region" {
  type = string
  default = "us-east-1"
}