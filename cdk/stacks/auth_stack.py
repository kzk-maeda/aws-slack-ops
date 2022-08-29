from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as _ddb,
    RemovalPolicy,
)


class Authenticator(Construct):

    def __init__(self, scope: "Construct", id: str) -> None:
        super().__init__(scope, id)

        self._table = _ddb.Table(
            self, 'Auth',
            table_name='Auth',
            partition_key={"name": "id", "type": _ddb.AttributeType.STRING},
            encryption=_ddb.TableEncryption.AWS_MANAGED,
            read_capacity=5,
            removal_policy=RemovalPolicy.DESTROY,
        )

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
