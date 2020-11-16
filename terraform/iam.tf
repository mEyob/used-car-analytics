data "aws_iam_policy_document" "ec2_assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "s3_access" {
  statement {
    effect = "Allow"

    actions = [
      "s3:*"
    ]

    resources = [
      aws_s3_bucket.s3_bucket.arn,
      "${aws_s3_bucket.s3_bucket.arn}/*",
    ]
  }
}

resource "aws_iam_role" "ec2_role" {
  name               = "s3-role"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json
}

resource "aws_iam_role_policy" "ec2_s3_access_role_policy" {
    name   = "ec2_s3_access_role_policy" 
    role   = aws_iam_role.ec2_role.name
    policy = data.aws_iam_policy_document.s3_access.json
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name  = "ec2_profile"
  role = aws_iam_role.ec2_role.name
}