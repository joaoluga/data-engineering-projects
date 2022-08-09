variable glue_job_name {
  type = string
}

variable role_arn {
  type = string
}

variable script_location {
  type = string
}

variable tags {
  type = map(string)
}

variable glue_version {
  type = string
  default = "3.0"
}

variable number_of_worker {
  type = number
  default = 2
}

variable worker_type {
  type    = string
  default = "Standard"
}

variable max_concurrent_runs {
  type = number
  default = 2
}

variable default_arguments {
  type = map(string)
  default = null
}

variable non_overridable_arguments {
  type = map(string)
  default = null
}

