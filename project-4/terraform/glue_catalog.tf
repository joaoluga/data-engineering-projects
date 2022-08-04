resource "aws_vpc_endpoint" "s3" {
  vpc_id       = data.aws_vpc.main.id
  service_name = "com.amazonaws.us-east-1.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids = [data.aws_route_table.default.id]
}

resource "aws_glue_connection" "s3_connection" {
  name = "s3-connection"
  connection_type = "NETWORK"

  physical_connection_requirements {
    availability_zone      = data.aws_subnet.default.availability_zone
    security_group_id_list = [data.aws_security_group.default.id]
    subnet_id              = data.aws_subnet.default.id
  }
}

resource "aws_glue_catalog_database" "refined_layer" {
  name = "${var.project_name}_refined"
  #location_uri = "s3://${aws_s3_bucket.emr.id}/data_lake/refined"
  location_uri = "s3://project4-emr/data_lake/layers/refined"
}

resource "aws_glue_catalog_database" "trusted_layer" {
  name = "${var.project_name}_trusted"
  #location_uri = "s3://${aws_s3_bucket.emr.id}/data_lake/trusted"
  location_uri = "s3://project4-emr/data_lake/layers/trusted"

}

resource "aws_glue_crawler" "refined_crawler" {
  database_name = aws_glue_catalog_database.refined_layer.name
  name          = "refined_layer"
  description   = "Crawler for the refined layer"
  role          = data.aws_iam_role.lab_role.arn

  s3_target {
    path = aws_glue_catalog_database.refined_layer.location_uri
    connection_name = aws_glue_connection.s3_connection.name
  }

  tags = local.default_tags
}

resource "aws_glue_crawler" "trusted_crawler" {
  database_name = aws_glue_catalog_database.trusted_layer.name
  name          = "trusted_layer"
  description   = "Crawler for the trusted layer"
  role          = data.aws_iam_role.lab_role.arn

  s3_target {
    path = aws_glue_catalog_database.trusted_layer.location_uri
    connection_name = aws_glue_connection.s3_connection.name
  }

  tags = local.default_tags
}