variable "project_name" {
  description = "Project name used as a resource prefix."
  type        = string
}

variable "region" {
  description = "AWS region."
  type        = string
  default     = "us-east-1"
}

variable "db_password" {
  description = "RDS master password."
  type        = string
  sensitive   = true
}

variable "db_username" {
  description = "RDS master username."
  type        = string
  default     = "shortener"
}

variable "db_name" {
  description = "RDS database name."
  type        = string
  default     = "shortener"
}

variable "instance_type" {
  description = "EC2 instance type."
  type        = string
  default     = "t3.micro"
}

variable "db_instance_class" {
  description = "RDS instance class."
  type        = string
  default     = "db.t3.micro"
}

variable "ssh_public_key" {
  description = "SSH public key material for the EC2 key pair (injected by platform)."
  type        = string
}
