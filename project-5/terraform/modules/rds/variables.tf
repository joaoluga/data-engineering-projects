variable rds_identifier {
  type = string
}

variable rds_name {
  type = string
}

variable rds_engine {
  type = string
  default = "postgres"
}

variable rds_engine_version {
  type = string
  default = "12"
}

variable rds_port {
  type = number
  default = 5432
}

variable vpc_security_group_ids {
  type = list(string)
}

variable subnet_ids {
  type = list(string)
}

variable tags {
  type = map(string)
}