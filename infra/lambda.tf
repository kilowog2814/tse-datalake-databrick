resource "aws_iam_role" "lambda" {
  name = "${var.lambda_function}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}


resource "aws_iam_policy" "lambda" {
  name = "${var.lambda_function}-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [

      # CloudWatch Logs
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      },

      # ECR - Permissão para Lambda baixar imagem
      {
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchGetImage",
          "ecr:GetDownloadUrlForLayer"

        ]
        Resource = "*"
      },

      {
        Effect = "Allow"
        Action = [
          "ecr:BatchCheckLayerAvailability",
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage"
        ]
        Resource = aws_ecr_repository.lambda.arn
      },

      # S3
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.tse_datalake_portifolio.arn,
          "${aws_s3_bucket.tse_datalake_portifolio.arn}/*"
        ]
      }
    ]
  })
}


resource "aws_iam_role_policy_attachment" "lambda" {
  role       = aws_iam_role.lambda.name
  policy_arn = aws_iam_policy.lambda.arn
}


resource "aws_lambda_function" "lambda" {
  function_name = var.lambda_function

  package_type = "Image"

  image_uri = "${aws_ecr_repository.lambda.repository_url}:latest"

  role = aws_iam_role.lambda.arn

  timeout     = var.timeout
  memory_size = var.memory_size

  depends_on = [
    aws_ecr_repository_policy.lambda
  ]
}

resource "aws_lambda_function" "bronze_lambda" {
  function_name = var.bronze_lambda_function

  package_type = "Image"

  image_uri = "${aws_ecr_repository.lambda.repository_url}:latest"

  role = aws_iam_role.lambda.arn

  timeout     = var.timeout
  memory_size = var.memory_size

  depends_on = [
    aws_ecr_repository_policy.lambda
  ]
}
