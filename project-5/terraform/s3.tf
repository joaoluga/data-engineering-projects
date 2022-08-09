resource "random_integer" "int" {
  min = 100000
  max = 500000
}

resource "aws_s3_bucket" "glue" {
  bucket = "${var.project_name}-glue-${random_integer.int.result}-${var.environment}"
}

resource "aws_s3_bucket_object" "data_lake" {
  bucket = aws_s3_bucket.glue.id
  key    = "data_lake/"
  source = "/dev/null"
}

resource "aws_s3_bucket_object" "packages" {
  bucket = aws_s3_bucket.glue.id
  key    = "packages/"
  source = "/dev/null"
}

resource "aws_s3_bucket_object" "src" {
  bucket = aws_s3_bucket.glue.id
  key    = "src/"
  source = "/dev/null"
}

resource "aws_ssm_parameter" "glue_bucket" {
  name        = "/glue/glue_bucket_name"
  description = "structured jdbc URL"
  type        = "SecureString"
  value       = aws_s3_bucket.glue.id

  tags = merge(local.default_tags, {Resource = "/glue/glue_bucket_name"})
}
