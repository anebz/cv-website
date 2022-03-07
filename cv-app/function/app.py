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
    today = datetime.now().strftime('%Y-%m-%d')

    # increment count by 1
    dbResponse = ddbClient.update_item(
        TableName=os.environ['TABLENAME'],
        Key={'date': {'S': today}},
        UpdateExpression="ADD #counter :increment",
        ExpressionAttributeNames={'#counter': 'count'},
        ExpressionAttributeValues={':increment': {'N': '1'}}
    )

    if dbResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
        return {'headers': {"Access-Control-Allow-Origin": "*",
                            "Access-Control-Allow-Methods": "GET",
                            "Access-Control-Allow-Headers": "Content-Type"},
        'statusCode': dbResponse['ResponseMetadata']['HTTPStatusCode'],
        'body': json.dumps({"Count": -1})}

    # get count
    getItemResponse = ddbClient.get_item(
        TableName=os.environ['TABLENAME'],
        Key={"date": {"S": today}}
    )
    httpscode = getItemResponse['ResponseMetadata']['HTTPStatusCode']
    count = getItemResponse['Item']['count']['N'] if httpscode == 200 else -1
    
    return {'headers': {"Access-Control-Allow-Origin": "*",
                        "Access-Control-Allow-Methods": "GET",
                        "Access-Control-Allow-Headers": "Content-Type"},
            'statusCode': httpscode,
            'body': json.dumps({"Count": count})}
