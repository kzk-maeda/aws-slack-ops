from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as _ddb,
    RemovalPolicy,
)
import boto3

TABLE_NAME = "Auth_cdk"


class Authenticator(Construct):

    def __init__(self, scope: "Construct", id: str) -> None:
        super().__init__(scope, id)

        self._table = _ddb.Table(
            self, 'Auth',
            table_name=TABLE_NAME,
            partition_key={"name": "user_id", "type": _ddb.AttributeType.STRING},
            encryption=_ddb.TableEncryption.AWS_MANAGED,
            read_capacity=5,
            removal_policy=RemovalPolicy.DESTROY,
        )
        # self._insert_initial_data()

        self._layer = _lambda.LayerVersion(
            self, 'AuthLayer',
            code=_lambda.Code.from_asset('lambda'),
            layer_version_name="auth",
        )

    @property
    def table(self):
        return self._table

    @property
    def layer(self):
        return self._layer
    
    def _insert_initial_data(self):
        ddb = boto3.resource('dynamodb')
        table = ddb.Table(TABLE_NAME)
        test_user_id = "test_id"

        test_user = table.get_item(
            Key={"user_id": test_user_id}
        )
        if test_user.get("Item"):
            return
        else:
            table.put_item(
                Item={
                    "user_id": "test_id",
                    "role": "user"
                }
            )
