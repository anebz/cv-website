import os
import boto3
import json
from datetime import datetime

ddbClient = boto3.client('dynamodb', region_name='eu-central-1')

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    dbresponse = ddbClient.update_item(
        TableName=os.environ['TABLENAME'],
        Key={'date': {'S': datetime.today().strftime('%Y-%m-%d')}},
        UpdateExpression="ADD #counter :increment",
        ExpressionAttributeNames={'#counter': 'count'},
        ExpressionAttributeValues={':increment': {'N': '1'}}
    )
    httpscode = dbresponse['ResponseMetadata']['HTTPStatusCode']
    return {'statusCode': httpscode,
            'body': json.dumps('Count updated' if httpscode == 200 else 'Error: count was not updated')}
