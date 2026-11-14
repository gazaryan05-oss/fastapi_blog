resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  tags                 = { Name = var.vpc_name }
}

resource "aws_subnet" "public" {
  count                   = length(var.cidr_public_subnet)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.cidr_public_subnet[count.index]
  availability_zone       = var.eu_availability_zone[count.index]
  map_public_ip_on_launch = true
  tags                    = { Name = "vika-public-subnet-${count.index}" }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
  tags   = { Name = "vika-igw" }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

resource "aws_route_table_association" "public" {
  count          = length(aws_subnet.public)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}
