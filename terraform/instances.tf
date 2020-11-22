resource "aws_vpc" "vpc_used_car_analytics" {
  cidr_block           = var.vpc_cidr_block
  enable_dns_hostnames = true

  tags = {
      Name = "vpc-used-car-analytics"
  }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.vpc_used_car_analytics.id

  tags = {
      Name = "igw-used-car-vpc"
  }
}
resource "aws_route_table" "rtable" {
  vpc_id = aws_vpc.vpc_used_car_analytics.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.gw.id
  }

  tags = {
    Name = "main-rt"
  }
}

resource "aws_subnet" "puplic_subnet" {
  vpc_id                  = aws_vpc.vpc_used_car_analytics.id
  cidr_block              = var.subnet_cidr_block
  map_public_ip_on_launch = true

  depends_on = [aws_internet_gateway.gw]
  tags = {
    Name = "public_subnet"
  }
}

resource "aws_route_table_association" "rtable_to_subnet" {
  subnet_id      = aws_subnet.puplic_subnet.id
  route_table_id = aws_route_table.rtable.id
}

resource "aws_security_group" "ec2_security_group" {
  name        = "ec2_security_group"
  description = "Allow SSH and HTTP requests"
  vpc_id      = aws_vpc.vpc_used_car_analytics.id

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

data "template_file" "ec2_userdata" {
  template = "${file("${path.cwd}/userdata.tpl")}"
}

resource "aws_instance" "scrapper" {
  ami                  = var.ami # eg. ubuntu 18.04 ami
  instance_type        = var.instance_type
  key_name             = var.key_name
  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name

  private_ip             = var.scrapper_ec2_pvt_ip
  subnet_id              = aws_subnet.puplic_subnet.id
  vpc_security_group_ids = [aws_security_group.ec2_security_group.id]

  user_data = data.template_file.ec2_userdata.template

  tags = {
      Name = "scrapper"
  }
}
