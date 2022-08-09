variable ecs_service_name {
  type = string
}

variable ecs_cluster_id {
  type = string
}

variable desired_count {
  type = number
  default = 1
}

variable launch_type {
  type = string
  default = "FARGATE"
}

variable deployment_maximum_percent {
  type = number
  default = null
}

variable deployment_minimum_percent {
  type = number
  default = null
}

variable health_check_grace_period_seconds {
  type = number
  default = null
}

variable ecs_service_security_groups {
  type = list(string)
}

variable ecs_service_subnets {
  type = list(string)
}

variable create_with_load_balancer {
  type = bool
  default = false
}

variable lb_target_group_arn {
  type = string
  default = null
}

variable lb_container_name {
  type = string
  default = null
}

variable lb_container_port {
  type = number
  default = null
}

variable task_name {
  type = string
}

variable execution_role_arn {
  type = string
}

variable task_role_arn {
  type = string
}

variable cpu {
  type = string
}

variable memory {
  type = string
}

variable container_definitions {
}

variable tags {
  type = map(string)
}

