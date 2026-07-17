resource "aws_ecr_repository_policy" "lambda" {
  repository = aws_ecr_repository.lambda.name

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [
      {
        Sid    = "LambdaECRAccess"
        Effect = "Allow"

        Principal = {
          Service = "lambda.amazonaws.com"
        }

        Action = [
          "ecr:BatchGetImage",
          "ecr:GetDownloadUrlForLayer",
          "ecr:SetRepositoryPolicy"
        ]
      }
    ]
  })
}

resource "aws_ecr_repository" "lambda" {
  name = var.ecr_repository

  image_scanning_configuration {
    scan_on_push = true
  }

  image_tag_mutability = "MUTABLE"
}
