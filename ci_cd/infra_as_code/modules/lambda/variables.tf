variable "source_stream_name" {
    type = string
  description = "Source kinesis Data stream name"
}

variable "source_stream_arn" {
  description = "Source kinesis Data stream arn"
}

variable "output_stream_name" {
  description = "Name of the output stream where all the events will be passed"
}

variable "output_stream_arn" {
  description = "ARN of the output stream where all the events will be passed"
}

variable "model_bucket" {
    description = "name of the bucket"
}
variable "lambda_function_name" {
  description = "Name of the lambda function"
}

variable "image_uri" {
  description = "ECR image uri"
}