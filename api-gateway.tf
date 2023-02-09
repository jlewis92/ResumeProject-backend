resource "aws_api_gateway_rest_api" "resume_project_gateway" {
  name        = "ResumeProjectGateway"
  description = "Terraform Resume Project Gateway definition"
}

# RESOURCES

resource "aws_api_gateway_resource" "visitor_gateway_resource" {
  rest_api_id = aws_api_gateway_rest_api.resume_project_gateway.id
  parent_id   = aws_api_gateway_rest_api.resume_project_gateway.root_resource_id
  path_part   = "visitor"
}

# METHODS

resource "aws_api_gateway_method" "visitor_gateway_method" {
  rest_api_id   = aws_api_gateway_rest_api.resume_project_gateway.id
  resource_id   = aws_api_gateway_resource.visitor_gateway_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "gateway_options_method" {
  rest_api_id   = aws_api_gateway_rest_api.resume_project_gateway.id
  resource_id   = aws_api_gateway_resource.visitor_gateway_resource.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

# RESPONSES

resource "aws_api_gateway_method_response" "visitor_gateway_response_200" {
  rest_api_id = aws_api_gateway_rest_api.resume_project_gateway.id
  resource_id = aws_api_gateway_method.visitor_gateway_method.resource_id
  http_method = aws_api_gateway_method.visitor_gateway_method.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = true
  }
  depends_on = [aws_api_gateway_method.gateway_options_method]
}

resource "aws_api_gateway_method_response" "options_200" {
  rest_api_id = aws_api_gateway_rest_api.resume_project_gateway.id
  resource_id = aws_api_gateway_method.gateway_options_method.resource_id
  http_method = aws_api_gateway_method.gateway_options_method.http_method
  status_code = "200"
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
  depends_on = [aws_api_gateway_method.gateway_options_method]
}

# INTEGRATIONS

resource "aws_api_gateway_integration" "lambda" {
  rest_api_id = aws_api_gateway_rest_api.resume_project_gateway.id
  resource_id = aws_api_gateway_method.visitor_gateway_method.resource_id
  http_method = aws_api_gateway_method.visitor_gateway_method.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.resume_project_lambda_func.invoke_arn
}

resource "aws_api_gateway_integration" "options_integration" {
  rest_api_id = aws_api_gateway_rest_api.resume_project_gateway.id
  resource_id = aws_api_gateway_method.gateway_options_method.resource_id
  http_method = aws_api_gateway_method.gateway_options_method.http_method
  type        = "MOCK"
  depends_on  = [aws_api_gateway_method.gateway_options_method]
}

# INTEGRATION RESPONSES

resource "aws_api_gateway_integration_response" "options_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.resume_project_gateway.id
  resource_id = aws_api_gateway_method.gateway_options_method.resource_id
  http_method = aws_api_gateway_method.gateway_options_method.http_method
  status_code = aws_api_gateway_method_response.options_200.status_code
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
    "method.response.header.Access-Control-Allow-Methods" = "'GET,OPTIONS,POST,PUT'",
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }
  depends_on = [aws_api_gateway_method_response.options_200]
}

# DEPLOYMENTS

resource "aws_api_gateway_deployment" "resume_project_gateway_deployment" {
  depends_on = [
    aws_api_gateway_integration.lambda
  ]

  rest_api_id = aws_api_gateway_rest_api.resume_project_gateway.id
  stage_name  = "prod"
}
