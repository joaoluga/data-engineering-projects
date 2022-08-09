resource "aws_s3_bucket" "athena_output" {
  bucket = "${var.project_name}-athena-output-${random_integer.int.result}-${var.environment}"
}

resource "aws_athena_data_catalog" "refined" {
  name        = "refined_catalog"
  description = "Glue based Data Catalog - Refined Layer"
  type        = "GLUE"

  parameters = {
    "catalog-id" = aws_glue_catalog_database.refined_layer.catalog_id
  }
}

resource "aws_athena_data_catalog" "trusted" {
  name        = "trusted_catalog"
  description = "Glue based Data Catalog - Trusted Layer"
  type        = "GLUE"

  parameters = {
    "catalog-id" = aws_glue_catalog_database.trusted_layer.catalog_id
  }
}

resource "aws_athena_workgroup" "de_group" {
  name = "data-engineering"

  configuration {
    enforce_workgroup_configuration    = true
    publish_cloudwatch_metrics_enabled = true

    result_configuration {
      output_location = "s3://${aws_s3_bucket.athena_output.bucket}/output/"
    }
  }
}