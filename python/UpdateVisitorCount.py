import boto3
import logging
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import json

ERROR_HELP_STRINGS = {
    # Operation specific errors
    'ConditionalCheckFailedException': 'Condition check specified in the operation failed, review and update the condition check before retrying',
    'TransactionConflictException': 'Operation was rejected because there is an ongoing transaction for the item, generally safe to retry with exponential back-off',
    'ItemCollectionSizeLimitExceededException': 'An item collection is too large, you\'re using Local Secondary Index and exceeded size limit of items per partition key.' +
                                                ' Consider using Global Secondary Index instead',
    # Common Errors
    'InternalServerError': 'Internal Server Error, generally safe to retry with exponential back-off',
    'ProvisionedThroughputExceededException': 'Request rate is too high. If you\'re using a custom retry strategy make sure to retry with exponential back-off.' +
                                              'Otherwise consider reducing frequency of requests or increasing provisioned capacity for your table or secondary index',
    'ResourceNotFoundException': 'One of the tables was not found, verify table exists before retrying',
    'ServiceUnavailable': 'Had trouble reaching DynamoDB. generally safe to retry with exponential back-off',
    'ThrottlingException': 'Request denied due to throttling, generally safe to retry with exponential back-off',
    'UnrecognizedClientException': 'The request signature is incorrect most likely due to an invalid AWS access key ID or secret key, fix before retrying',
    'ValidationException': 'The input fails to satisfy the constraints specified by DynamoDB, fix input before retrying',
    'RequestLimitExceeded': 'Throughput exceeds the current throughput limit for your account, increase account level throughput before retrying',
}


import os

def isRunningInAws():
    is_aws = True if os.environ.get("AWS_DEFAULT_REGION") else False
    return is_aws

def getClient(is_aws: bool, region_name: str):
    if (is_aws):
        dynamodb_client = boto3.client('dynamodb', region_name=region_name)
    else:
        dynamodb_client = boto3.client('dynamodb', endpoint_url="http://localhost:8000")
    return dynamodb_client

def create_update_item_input(table_name: str):
    return {
        "TableName": table_name,
        "Key": {
            "PK": {"S":"resumeProject"}
        },
        "UpdateExpression": "SET #visitorCount = #visitorCount + :increment",
        "ExpressionAttributeNames": {"#visitorCount":"VisitorCount"},
        "ExpressionAttributeValues": {":increment": {"N":"1"}},
        "ReturnValues":"UPDATED_NEW"
    }

def execute_update_item(dynamodb_client, input):
    try:
        response = dynamodb_client.update_item(**input)
        print("Successfully updated item.")
        return response
    except ClientError as error:
        handle_error(error)
    except BaseException as error:
        print("Unknown error while updating item: " + error.response['Error']['Message'])


def handle_error(error):
    error_code = error.response['Error']['Code']
    error_message = error.response['Error']['Message']

    error_help_string = ERROR_HELP_STRINGS[error_code]

    logging.warning('[{error_code}] {help_string}. Error message: {error_message}'
          .format(error_code=error_code,
                  help_string=error_help_string,
                  error_message=error_message))


def lambda_handler(event, context):
    is_aws = isRunningInAws()
    print("Running in AWS: ", is_aws)

    table_name = os.getenv('table_name')
    region = os.getenv('AWS_DEFAULT_REGION')

    # setup dynamo client
    dynamodb_client = getClient(is_aws, region)
   
    # Create the dictionary containing arguments for the update_item call
    update_item_input = create_update_item_input(table_name)

    # Call DynamoDB's update_item API
    response = execute_update_item(dynamodb_client, update_item_input)
    lambdaResponse = {
        'statusCode': json.dumps(response["ResponseMetadata"]["HTTPStatusCode"]),
        'body': json.dumps(response["Attributes"]["VisitorCount"]["N"]),
        'headers' : {
            'Access-Control-Allow-Origin' : '*'
        }
    }

    print(lambdaResponse)

    return(lambdaResponse)