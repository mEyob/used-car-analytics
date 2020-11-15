resource "aws_vpc" "vpc-used-car-analytics" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.vpc-used-car-analytics.id
}

resource "aws_subnet" "puplic_subnet" {
  vpc_id                  = aws_vpc.vpc-used-car-analytics.id
  cidr_block              = "10.0.0.0/24"
  map_public_ip_on_launch = true

  depends_on = [aws_internet_gateway.gw]
}

resource "aws_security_group" "ec2_security_group" {
  name        = "ec2_security_group"
  description = "Allow SSH and HTTP requests"
  vpc_id      = aws_vpc.vpc-used-car-analytics.id

  ingress {
    description = "SSH from anywhere"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP from anywhere"
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "used-car-analytics-sg"
  }
}

resource "aws_instance" "scrapper" {
  ami           = "ami-00ddb0e5626798373" # ubuntu 18.04 ami
  instance_type = "t2.micro"

  private_ip = "10.0.0.5"
  subnet_id  = aws_subnet.puplic_subnet.id
  vpc_security_group_ids = [aws_security_group.ec2_security_group.id]
  tags = {
      Name = "scrapper"
  }
}
