data "aws_vpc" "main" {
  filter {
    name   = "state"
    values = ["available"]
  }
}

data "aws_subnets" "subnets" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.main.id]
  }
}

data "aws_iam_role" "lab_role" {
  name = "LabRole"
}

data "aws_security_group" "default" {
  name = "default"
}

data "aws_subnet" "default" {
  availability_zone = "us-east-1b"
}

data "aws_route_table" "default" {
  vpc_id = data.aws_vpc.main.id
}
