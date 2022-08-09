module "etl_job" {
  source = "./modules/glue_jobs"
  glue_job_name = "etl_job"
  role_arn = data.aws_iam_role.lab_role.arn
  script_location = "s3://${aws_s3_bucket.glue.bucket}/src/job_template.py"
  max_concurrent_runs = 2
  default_arguments = {
    "--additional-python-modules"             = "psycopg2-binary,Unidecode,fastparquet,sqlalchemy"
    "--extra-py-files"                        = "s3://${aws_s3_bucket.glue.bucket}/packages/packages.zip"
    "--enable-s3-parquet-optimized-committer" = "true"
    "--enable-rename-algorithm-v2"            = "true"
    "--entity_name"                           = ""
    "--etl_phase"                             = ""
  }
  tags = merge(local.default_tags, {Resource = "/glue/glue_bucket_name"})
}