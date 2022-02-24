# Cloud challenge

CloudFormation: don't use custom names for resources.

To deploy template to stack:

```bash
aws cloudformation deploy --template-file main.yaml --stack-name cv-website --capabilities CAPABILITY_NAMED_IAM
```
Upload index and website files to bucket

```bash
aws s3 cp static/. s3://anebz-cv/ --recursive
```

Add item to DynamoDB table in Python:

```python
import boto3

tablename = 'cvtable'
ddbClient = boto3.client('dynamodb', region_name='eu-central-1')
dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
ddbTable = dynamodb.Table(tablename)

putResponse = ddbClient.put_item(
    Item = {
        "date": {
            "S": "2022-02-23"
        },
        "count": {
            "N": "1"
        }
    },
    TableName = tablename
)
```

Increment count in Table with Python:

```python
dbresponse = ddbClient.update_item(
    TableName=tablename,
    Key={'date': {'S': '2022-02-24'}},
    UpdateExpression="ADD #counter :increment",
    ExpressionAttributeNames={'#counter': 'count'},
    ExpressionAttributeValues={':increment': {'N': '1'}}
)
```

Connect Lambda to API Gateway:

1. Create Lambda function
2. Write Python code to write to DDB table
3. Give DDB permission to Role
4. Create API and connect it to Lambda

