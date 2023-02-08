data "archive_file" "zip_the_python_code" {
  type        = "zip"
  source_file = "${path.module}/python/UpdateVisitorCount.py"
  output_path = "${path.module}/python/resume-project-python.zip"
}

resource "aws_lambda_function" "resume_project_lambda_func" {
  filename         = data.archive_file.zip_the_python_code.output_path
  source_code_hash = data.archive_file.zip_the_python_code.output_base64sha256
  function_name    = "Resume_Project_Lambda_Function"
  role             = aws_iam_role.resume_project_role.arn
  handler          = "UpdateVisitorCount.lambda_handler"
  runtime          = "python3.8"
  environment {
    variables = {
      table_name = var.table_name
    }
  }
  depends_on = [aws_iam_role_policy_attachment.attach_iam_policy_to_iam_role]
}

resource "aws_cloudwatch_log_group" "lambda_function" {
  name              = "/aws/lambda/Test_Lambda_Function"
  retention_in_days = 30
}

resource "aws_lambda_permission" "lambda_gateway_access" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.resume_project_lambda_func.function_name
  principal     = "apigateway.amazonaws.com"

  # The /*/* portion grants access from any method on any resource
  # within the API Gateway "REST API".
  source_arn = "${aws_api_gateway_rest_api.resume_project_gateway.execution_arn}/*/*"
}