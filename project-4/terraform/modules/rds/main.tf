resource "random_password" "rds_pwd" {
  length           = 24
  special          = false
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "aws_db_instance" "rds" {
  identifier                = var.rds_identifier
  allocated_storage         = 5
  backup_retention_period   = 1
  backup_window             = "01:00-01:30"
  maintenance_window        = "sun:03:00-sun:03:30"
  multi_az                  = false
  engine                    = var.rds_engine
  engine_version            = var.rds_engine_version
  instance_class            = "db.t2.micro"
  db_name                   = var.rds_name
  username                  = "root"
  password                  = random_password.rds_pwd.result
  port                      = var.rds_port
  db_subnet_group_name      = aws_db_subnet_group.subnet_group.id
  vpc_security_group_ids    = var.vpc_security_group_ids
  skip_final_snapshot       = true
  publicly_accessible       = false
  tags                      = merge(var.tags, {Resource = "rds-${var.rds_identifier}"})
}

resource "aws_db_subnet_group" "subnet_group" {
  name = "${var.rds_identifier}-subnet-group"
  subnet_ids = var.subnet_ids
  tags = merge(var.tags, {Resource = "${var.rds_identifier}-subnet-group"})
}

resource "aws_ssm_parameter" "root_pwd" {
  name        = "/rds/${var.rds_identifier}/password"
  description = "root password"
  type        = "SecureString"
  value       = random_password.rds_pwd.result

  tags = merge(var.tags, {Resource = "ssm-/rds/${var.rds_identifier}/password"})
}

resource "aws_ssm_parameter" "sqlalchemy_conn" {
  name        = "/rds/${var.rds_identifier}/sqlalchemy_conn"
  description = "structured sqlalchemy URL"
  type        = "SecureString"
  value       = "postgresql+psycopg2://${aws_db_instance.rds.username}:${random_password.rds_pwd.result}@${aws_db_instance.rds.address}:${var.rds_port}/${var.rds_name}"

  tags = merge(var.tags, {Resource = "ssm-/rds/${var.rds_identifier}/sqlalchemy_conn"})
}

resource "aws_ssm_parameter" "jdbc_conn" {
  name        = "/rds/${var.rds_identifier}/jdbc_conn"
  description = "structured jdbc URL"
  type        = "SecureString"
  value       = "jdbc:postgresql://${aws_db_instance.rds.address}:${var.rds_port}/${var.rds_name}?user=${aws_db_instance.rds.username}&password=${random_password.rds_pwd.result}"

  tags = merge(var.tags, {Resource = "ssm-/rds/${var.rds_identifier}/jdbc_conn"})
}
