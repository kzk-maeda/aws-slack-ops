import json
import boto3


class Authenticator():
    
    def __init__(self) -> None:
        self.ddb = boto3.resource('dynamodb')
        self.table = self.ddb.Table("Auth_cdk")

    def has_role(self, user_id: str) -> bool:
        item = self.table.get_item(
            Key={"user_id": user_id}
        )
        print(item)

        if item.get('Item'):
            return True
        else:
            return False


def handler(user_id: str) -> bool:
    print("auth.handler")

    authenticator = Authenticator()
    return authenticator.has_role(user_id)
