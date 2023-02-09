variable "region" {
  description = "The aws region"
  type        = string
  sensitive   = true
}

variable "account_id" {
  description = "The aws account"
  type        = string
  sensitive   = true
}

variable "table_name" {
  description = "The aws table"
  type        = string
  sensitive   = true
}

provider "aws" {
  region  = var.region
}