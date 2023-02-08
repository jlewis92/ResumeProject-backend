import unittest
import os
from unittest import mock
import boto3
from unittest.mock import MagicMock
from moto import mock_dynamodb

from UpdateVisitorCount import *


class TestSum(unittest.TestCase):
    
    @mock.patch.dict(os.environ, {"AWS_DEFAULT_REGION": "SOME_VALUE"})
    def test_isRunningInAws_isTrue(self):
        self.assertTrue(isRunningInAws())

    @mock.patch.dict(os.environ, {"AWS_DEFAULT_REGION": ""})
    def test_isRunningInAws_isTrue(self):
        self.assertFalse(isRunningInAws())

    @mock.patch.dict(os.environ, {"AWS_DEFAULT_REGION": ""})
    def test_create_update_item_input_returnsInput(self):
        response = create_update_item_input("some_table")
        self.assertEqual(response["TableName"], "some_table")
        self.assertEqual(response["Key"]["PK"]["S"], "resumeProject")

    @mock.patch.dict(os.environ, {"AWS_DEFAULT_REGION": "us-east-2"})
    @mock_dynamodb
    def test_update_resume_project_table(self):
        boto3.DEFAULT_SESSION = None
        client = boto3.client('dynamodb')

        table_name = 'some-table'
        client.create_table(TableName=table_name,
        KeySchema=[{'AttributeName': 'PK','KeyType': 'HASH'},{'AttributeName': 'VisitorCount','KeyType': 'N'}],
        BillingMode="PAY_PER_REQUEST",
        AttributeDefinitions=[{'AttributeName': 'PK','AttributeType': 'S'},{'AttributeName': 'VisitorCount','AttributeType': 'N'}])

        item = {
            "TableName": "some-table",
            "Item": {
                "PK": {"S":"resumeProject"}, 
                "VisitorCount": {"N":"2"}
            }
        }

        itemTwo = {
            "TableName": "some-table",
            "Key": {
                "PK": {"S":"resumeProject"}
            },
            "UpdateExpression": "SET #visitorCount = #visitorCount + :increment",
            "ExpressionAttributeNames": {"#visitorCount":"VisitorCount"},
            "ExpressionAttributeValues": {":increment": {"N":"1"}},
            "ReturnValues":"UPDATED_NEW"
        }

        # res = client.put_item(**item)
        # resTwo = client.update_item(**itemTwo)
        #input = create_update_item_input()
        #result = execute_update_item(client, input)
        #self.assertEqual(200, result['ResponseMetadata']['HTTPStatusCode'])

if __name__ == '__main__':
    unittest.main()