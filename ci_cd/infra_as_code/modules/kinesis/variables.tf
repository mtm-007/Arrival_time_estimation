variable "stream_name" {
  type = string
  description = "kinesis stream name"
}

variable "shard_count" {
  type = number
  description = "kinesis stream shard count"
}

variable "retention_period" {
  type = number
  description = "kinesis stream retention period"
}

variable "shard_level_metrics" {
  type =  list(string)
  description = "kinesis stream shard_level_metrics "
  default = [ 
    "IncomingBytes",
    "OutgoingBytes",
    "OutgoingRecords",
    "ReadProvisionedThroughputExceeded",
    "WriteProvisionedThroughputExceeded",
    "IncomingRecords",
    "IteratorAgeMilliseconds"
    ]
}
variable "tags" {
  description = "Tags for kinesis stream"
  default = "mlop-zm"
}