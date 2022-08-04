variable alb_name {
  type = string
}

variable subnets_ids {
  type = list(string)
}

variable security_groups {
  type = list(string)
}

variable vpc_id {
  type = string
}

#variable target_group_port {
#  type = number
#}

variable tags {
  type = map(string)
}

# Default values

variable target_type {
  type = string
  default = "ip"
}

variable health_check_interval {
  type = number
  default = 60
}

variable health_check_path {
  type = string
  default = "/health"
}

variable health_check_timeout {
  type = number
  default = 5
}

variable health_check_healthy_threshold {
  type = number
  default = 5
}

variable health_check_unhealthy_threshold {
  type = number
  default = 3
}