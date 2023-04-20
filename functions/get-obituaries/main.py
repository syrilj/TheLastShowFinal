import boto3
from boto3.dynamodb.conditions import Key

# create a dynamodb resource
dynamodb_resource = boto3.resource("dynamodb", region_name="ca-central-1")
table_name = "lastshow-30144227"

# create a dynamodb table object
table = dynamodb_resource.Table(table_name)

def lambda_handler(event, context):
    http_method = event["requestContext"]["http"]["method"].lower()
    obituaries = []
    if http_method == "get":
        #get uuid from header
        uuid = event["headers"]["uuid"]

        response = table.query(
            TableName = table_name,
            KeyConditionExpression=Key("uuid").eq(uuid)
        )
        obituaries = response["Items"]

    return obituaries

