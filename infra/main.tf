terraform {
  required_providers {
    aws = {
      version = ">= 4.0.0"
      source  = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region = "ca-central-1"
}

# two lambda functions w/ function url
# one dynamodb table
# roles and policies as needed
# step functions (if you're going for the bonus marks)


# read the docs: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/dynamodb_table
resource "aws_dynamodb_table" "lastshow-30144227" {
  name         = "lastshow-30144227"
  billing_mode = "PROVISIONED"

  # up to 8KB read per second (eventually consistent)
  read_capacity = 1

  # up to 1KB per second
  write_capacity = 1


  hash_key = "uuid"
  range_key = "name"
  
  attribute {
    name = "uuid"
    type = "S"
  }
  attribute {
    name = "name"
    type = "S"
  }


}


resource "aws_iam_role" "iam_for_lambda_lastshow" {
  name = "iam_for_lambda_lastshow"

  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Principal" : {
          "Service" : "lambda.amazonaws.com"
        },
        "Action" : "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "dynamodb-lambda-policy-lastshow" {
  name = "dynamodb_lambda_policy_lastshow"
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : ["dynamodb:*", "logs:*", "ssm:GetParametersByPath", "polly:SynthesizeSpeech"],
        "Resource" : [aws_dynamodb_table.lastshow-30144227.arn, "arn:aws:logs:*:*:*", "*", "*"]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach" {

  role = aws_iam_role.iam_for_lambda_lastshow.name
  policy_arn = aws_iam_policy.dynamodb-lambda-policy-lastshow.arn

}

data "archive_file" "get-obituaries-archive" {
  source_dir = "../functions/get-obituaries"
  output_path = "get-obituaries.zip"
  type        = "zip"
}


resource "aws_lambda_function" "get-obituaries" {
  role          = aws_iam_role.iam_for_lambda_lastshow.arn
  handler       = "main.lambda_handler"
  function_name = "get-obituaries-30145947"
  filename      = "get-obituaries.zip"
  source_code_hash = data.archive_file.get-obituaries-archive.output_base64sha256

  runtime = "python3.9"
}

# create a Function URL for Lambda 
# see the docs: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function_url
resource "aws_lambda_function_url" "get-obituaries-url" {
  function_name      = aws_lambda_function.get-obituaries.function_name
  authorization_type = "NONE"

  cors {
    allow_credentials = true
    allow_origins     = ["*"]
    allow_methods     = ["GET"]
    allow_headers     = ["*"]
    expose_headers    = ["keep-alive", "date"]
  }
}

# show the Function URL after creation
output "get-obituaries_url" {
  value = aws_lambda_function_url.get-obituaries-url.function_url
}

data "archive_file" "create-obituary-archive" {
  source_dir = "../functions/create-obituary"
  output_path = "create-obituary.zip"
  type        = "zip"
}

resource "aws_lambda_function" "create-obituary" {
  role          = aws_iam_role.iam_for_lambda_lastshow.arn
  handler       = "main.lambda_handler"
  function_name = "create-obituary-30145947"
  filename      = "create-obituary.zip"
  source_code_hash = data.archive_file.create-obituary-archive.output_base64sha256

  runtime = "python3.9"
}

# create a Function URL for Lambda 
# see the docs: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function_url
resource "aws_lambda_function_url" "create-obituary-url" {
  function_name      = aws_lambda_function.create-obituary.function_name
  authorization_type = "NONE"

  cors {
    allow_credentials = true
    allow_origins     = ["*"]
    allow_methods     = ["POST"]
    allow_headers     = ["*"]
    expose_headers    = ["keep-alive", "date"]
  }
}

# show the Function URL after creation
output "create-obituary_url" {
  value = aws_lambda_function_url.create-obituary-url.function_url
}
