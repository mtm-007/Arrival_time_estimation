variable "ecr_repo_name" {
  type = string
  description = "ecr repo name"
}

variable "ecr_image_tag" {
  type =        string
  description = "ECR image repo"
  default =     "latest"
}

variable "lambda_function_local_path" {
  type = string
  description = "Local path to lambda function/python script"
}

variable "docker_image_local_path" {
  type = string
  description = "local path to docker image"
}

variable "region" {
  type = string
  description = "aws region"
  default = "us-east-1"
}

variable "account_id" {
  
}