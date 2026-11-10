
variable "region" {
  type = string
  default = "us-east-1"
}

variable "owner" {
  type    = string
  default = "fvrsn"
}

variable "environment" {
  type    = string
  default = "sandbox"
}


//// EC2 ////

variable "aws_instance_name" {
  description = "AWS EC2 Instance Name"
  type        = string
}

variable "aws_instance_type" {
  description = "AWS EC2 Instance Type"
  type        = string
}


//// NTW ////

variable "vpc_cidr_block" {
  description = "Allowed CIDR blocks for VPC"
  type        = string
}

variable "sub_public_cidr_block" {
  description = "Allowed CIDR blocks for Public Subnet"
  type        = string
}

variable "sub_private_cidr_block" {
  description = "Allowed CIDR blocks for Private Subnet"
  type        = string
}
