resource "aws_ecr_repository" "lambda" {
  name = var.ecr_repository_name

  image_scanning_configuration {
    scan_on_push = true
  }

  image_tag_mutability = "MUTABLE"
}
