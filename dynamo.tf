resource "aws_dynamodb_table" "resume_project_table" {
  name         = var.table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "PK"
  table_class  = "STANDARD"
  attribute {
    name = "PK"
    type = "S"
  }

  tags = {
    "project" = "resume project"
  }
}
