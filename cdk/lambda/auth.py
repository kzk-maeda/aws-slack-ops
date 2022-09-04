import json
import boto3
from enum import Enum


class Role(Enum):
    Admin = "admin"
    User = "user"


class Authenticator():
    
    def __init__(self, user_id: str) -> None:
        self.ddb = boto3.resource('dynamodb')
        self.table = self.ddb.Table("Auth_cdk")
        self.user_id = user_id
        self.item = {}
    
    def authenticate(self, role: str):
        if not self._has_id():
            return False
        
        if not self._has_role(role):
            return False
        
        return True

    def _has_id(self) -> bool:
        self.item = self.table.get_item(
            Key={"user_id": self.user_id}
        )
        print(self.item)

        if self.item.get('Item'):
            return True
        else:
            return False

    def _has_role(self, required_role: str = Role.User.value) -> bool:
        role = self.item["Item"]["role"]
        has_role = False
        if required_role == Role.Admin.value:
            has_role = True if role == Role.Admin.value else False
        elif required_role == Role.User.value:
            has_role = True if role == Role.Admin.value or role == Role.User.value else False
        else:
            print('Invalid Role Required')

        return has_role

