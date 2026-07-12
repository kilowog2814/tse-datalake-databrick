resource "aws_s3_bucket" "tse-datalake-portifolio" {
  bucket = var.bucket
  acl    = "private"

  tags = {
    origem    = "tse"
    projeto   = "datalake"
    managedBy = "terraform"
  }
}

