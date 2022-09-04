import os
from typing import List
from unicodedata import name
from aws_cdk import (
    # Duration,
    Stack,
    aws_lambda as _lambda,
    aws_chatbot as _chatbot,
    aws_iam as _iam,
)
from constructs import Construct

from .auth_stack import Authenticator


class CdkStack(Stack):

    def __init__(
        self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        slack_channel_config_name = os.getenv('SLACK_CHANNEL_CONFIG_NAME') or ""
        slack_workspace_id = os.getenv('SLACK_WORKSPACE_ID') or ""
        slack_channel_id = os.getenv('SLACK_CHANNEL_ID') or ""
        if "" in [slack_channel_config_name, slack_workspace_id, slack_channel_id]:
            raise
        
        ### fron Layer
        authenticator = Authenticator(
            self, "Authenticator"
        )

        ### Lambda Resources
        main_lambda = _lambda.Function(
            self, 'MainHandler',
            function_name="main_cdk",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset('lambda'),
            handler='main.handler',
            layers=[authenticator.layer]
        )
        authenticator.table.grant_read_write_data(main_lambda)

        ### Chatbot Resources
        slack_bot = _chatbot.SlackChannelConfiguration(
            self, 'TestChannel1',
            slack_channel_configuration_name=slack_channel_config_name,
            slack_workspace_id=slack_workspace_id,
            slack_channel_id=slack_channel_id
        )

        slack_bot.add_to_role_policy(_iam.PolicyStatement(
            effect=_iam.Effect.ALLOW,
            actions=["lambda:*"
            ],
            resources=[main_lambda.function_arn]
        ))
