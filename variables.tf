
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

variable "instance_name" {
  description = "AWS EC2 Instance Name"
  type        = string
  default     = ""
}

variable "AWS_INSTANCE_TYPE" {
  description = "AWS EC2 Instance Type"
  type        = string
  default     = "t2.micro"
}

variable "AWS_AMI" {
  description = "AWS AMI ID"
  type        = string
  default     = ""
}

//// NTW ////

variable "vpc_cidr_block" {
  description = "Allowed CIDR blocks for VPC"
  type        = string
}

variable "PUBLIC_IP" {
  description = "Allowed CIDR blocks for Public IP"
  type        = string
}

variable "sub_public_availability_zone" {
  description = "Allowed CIDR blocks for Public Subnet Availability Zone"
  type        = string
}

variable "sub_public_cidr_block" {
  description = "Allowed CIDR blocks for Public Subnet"
  type        = string
}

variable "sub_private_availability_zone" {
  description = "Allowed CIDR blocks for Private Subnet Availability Zone"
  type        = string
}

variable "sub_private_cidr_block" {
  description = "Allowed CIDR blocks for Private Subnet"
  type        = string
}
