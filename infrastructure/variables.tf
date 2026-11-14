variable "vpc_cidr" { default = "10.0.0.0/16" }
variable "vpc_name" { default = "vika-jenkins-vpc" }
variable "cidr_public_subnet" { default = ["10.0.1.0/24", "10.0.2.0/24"] }
variable "eu_availability_zone" { default = ["eu-west-1a", "eu-west-1b"] }
variable "ec2_ami_id" { default = "ami-0694d931cee176e7d" } # Ubuntu 22.04 eu-west-1
variable "public_key" { type = string }
