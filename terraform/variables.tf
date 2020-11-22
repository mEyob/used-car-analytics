variable bucket_name {
    description = "S3 bucket name for storing scrapped car listing prices"
    type        = string    
}

variable ami {
    description = "Machine image for EC2"
    type        = string
}

variable instance_type {
    description = "EC2 instance type"
    type        = string
}

variable key_name {
    description = "AWS access key name to be used to securely access EC2"
    type        = string
}

variable scrapper_ec2_pvt_ip {
    description = "Web scrapper ec2's private ip"
    type        = string
}

variable vpc_cidr_block {
    description = "CIDR block of the VPC"
    type        = string
}

variable subnet_cidr_block {
    description = "CIDR block for the public subnet"
    type        = string
}

variable lambda_function_file {
    description = "Filename of the python lambda function to be executed"
    type        = string
}

variable lambda_function_name {
    description = "Name of lambda function to be created"
    type        = string
}

variable lambda_handler {
    description = "The lambda handler function"
    type        = string
}