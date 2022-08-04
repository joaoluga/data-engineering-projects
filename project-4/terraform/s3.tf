resource "random_integer" "int" {
  min = 10000
  max = 50000
}

resource "aws_s3_bucket" "emr" {
  bucket = "${var.project_name}-emr-${random_integer.int.result}-${var.environment}"
}

resource "aws_s3_bucket_object" "data_lake" {
  bucket = aws_s3_bucket.emr.id
  key    = "data_lake/"
  source = "/dev/null"
}

resource "aws_s3_bucket_object" "bootstrap_actions" {
  bucket = aws_s3_bucket.emr.id
  key    = "bootstrap_actions/"
  source = "/dev/null"
}

resource "aws_s3_bucket_object" "packages" {
  bucket = aws_s3_bucket.emr.id
  key    = "packages/"
  source = "/dev/null"
}

resource "aws_s3_bucket_object" "src" {
  bucket = aws_s3_bucket.emr.id
  key    = "src/"
  source = "/dev/null"
}

resource "aws_ssm_parameter" "emr_bucket" {
  name        = "/emr/emr_bucket_name"
  description = "structured jdbc URL"
  type        = "SecureString"
  value       = aws_s3_bucket.emr.id

  tags = merge(local.default_tags, {Resource = "/emr/emr_bucket_name"})
}
