resource "random_integer" "int" {
  min = 10000
  max = 50000
}

resource "aws_s3_bucket" "airflow_logs" {
  bucket = "${var.project_name}-${random_integer.int.result}-airflow-logs-${var.environment}"
}