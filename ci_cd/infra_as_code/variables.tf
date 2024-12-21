variable "aws_region" {
    description = "aws region to create resourcess"
    default = "us-east-1"
}

variable "project_id" {
    description = "project Id"
    default = "tf-mlop-zm"
}

variable "source_stream_name" {
  description = "source stream name"
  #default = "ride-events-stg"
}

variable "output_stream_name" {
  description = "source stream name"
  #default = "ride-events-stg"
}

variable "model_bucket" {
  description = "model s3 bucket"
  #default = "stg-mlflow-models" #can use the already set mlflow artifact stored in s3 
}

variable "lambda_function_local_path" {
  description = "local path to lambda function"
}

variable "docker_image_local_path" {
  description = "local path to docker image"
}

variable "ecr_repo_name" {
  description = "ECR repo name"
  
}

variable "lambda_function_name" {
  description = "value"
}