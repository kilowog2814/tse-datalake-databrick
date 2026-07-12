resource "aws_lambda_function" "lambda" {
  function_name = var.lambda_function

  package_type = "Image"

  image_uri = "${aws_ecr_repository.lambda.repository_url}:latest"

  role = aws_iam_role.lambda.arn

  timeout     = var.timeout
  memory_size = var.memory_size
}
