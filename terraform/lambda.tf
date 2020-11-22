data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
 
    principals {
      type = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_execution_role" {
   name = "transformer-lambda-role"
   assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json

 }

data "aws_iam_policy_document" "lambda_cloudwatch_and_ec2_access" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
 
    resources = [
      "*",
    ]
  }
  statement {
      effect = "Allow"
      actions = [
        "ec2:Start*",
        "ec2:Stop*"
      ]
      resources = [
          "*",
      ] 
    }
}

resource "aws_iam_role_policy" "lambda-cloudwatch-log-group" {
  name = "lambda-cloudwatch-log-and-ec2-role-policy"
  role = aws_iam_role.lambda_execution_role.name
  policy = data.aws_iam_policy_document.lambda_cloudwatch_and_ec2_access.json
}

data "archive_file" "lambda_function" { 
  type = "zip"
  source_file = var.lambda_function_file
  output_path = "lambda_function.zip"
}

resource "aws_lambda_function" "transformerLambda" {
  filename = data.archive_file.lambda_function.output_path
  function_name = var.lambda_function_name
  role = aws_iam_role.lambda_execution_role.arn
  handler = var.lambda_handler
  runtime = "python3.7"
  timeout = 180
  source_code_hash = base64sha256(filebase64(data.archive_file.lambda_function.output_path))
}