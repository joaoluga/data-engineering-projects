module analytics_rds {
  source = "./modules/rds"
  rds_identifier = "analytics-db-${var.environment}"
  rds_name = "analytics"
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  subnet_ids = data.aws_subnets.subnets.ids
  tags = local.default_tags
}