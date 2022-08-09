resource "aws_glue_job" "etl_job" {
  name              = var.glue_job_name
  role_arn          = var.role_arn
  glue_version      = var.glue_version
  number_of_workers = var.number_of_worker
  worker_type       = var.worker_type

  command {
    script_location = var.script_location
  }

  execution_property {
    max_concurrent_runs = var.max_concurrent_runs
  }

  default_arguments = merge(var.default_arguments, {
    "--continuous-log-logGroup"          = aws_cloudwatch_log_group.glue.name
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-continuous-log-filter"     = "true"
    "--enable-metrics"                   = ""
  })

  non_overridable_arguments = var.non_overridable_arguments

  tags = merge(var.tags, {Resource = "glue_job-${var.glue_job_name}"})
}

resource "aws_cloudwatch_log_group" "glue" {
  name = "/glue/jobs/${var.glue_job_name}"
  retention_in_days = 1
  tags = merge(var.tags, {Resource = "cw_log_group-/glue/jobs/${var.glue_job_name}"})
}