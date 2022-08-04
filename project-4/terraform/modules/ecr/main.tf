resource "aws_ecr_repository" "docker_repository" {
  name = var.ecr_name
  tags = merge(var.tags, {Resource = "ecr-${var.ecr_name}"})
}

resource "aws_ecr_lifecycle_policy" "docker_repository_lifecycle" {
  repository = aws_ecr_repository.docker_repository.name

  policy = <<EOF
{
    "rules": [
        {
            "rulePriority": 1,
            "description": "Keep only the latest 3 images",
            "selection": {
                "tagStatus": "any",
                "countType": "imageCountMoreThan",
                "countNumber": 3
            },
            "action": {
                "type": "expire"
            }
        }
    ]
}
EOF
}