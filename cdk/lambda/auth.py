import json
import boto3

def handler(user_id: str) -> bool:
    print("auth.handler")

    ddb = boto3.client('dynamodb')
    tables = ddb.scan(TableName='Auth')
    print(tables)

    return True
