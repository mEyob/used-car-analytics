resource "aws_cloudwatch_event_rule" "invoke_starter_lambda" {
    name = "start-every-monday"
    description = "Fires every week on Monday at 2am"
    schedule_expression = "cron(0 2 ? * 1 *)"
}

resource "aws_cloudwatch_event_rule" "invoke_stopper_lambda" {
    name = "stop-every-monday"
    description = "Fires every week on Monday at 4am"
    schedule_expression = "cron(0 4 ? * 1 *)"
}

resource "aws_cloudwatch_event_target" "starter_lambda_target" {
    rule = aws_cloudwatch_event_rule.invoke_starter_lambda.name
    target_id = aws_lambda_function.controller_lambda.id
    arn = aws_lambda_function.controller_lambda.arn
}

resource "aws_cloudwatch_event_target" "stopper_lambda_target" {
    rule = aws_cloudwatch_event_rule.invoke_stopper_lambda.name
    target_id = aws_lambda_function.controller_lambda.id
    arn = aws_lambda_function.controller_lambda.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.controller_lambda.function_name
    principal = "events.amazonaws.com"
    # source_arn = aws_cloudwatch_event_rule.invoke_starter_lambda.arn
}