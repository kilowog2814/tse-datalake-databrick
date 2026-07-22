resource "aws_s3_bucket" "tse_datalake_portifolio" {
  bucket = var.bucket
  acl    = "private"

  tags = {
    origem    = "tse"
    projeto   = "datalake"
    managedBy = "terraform"
  }
}

