import json
from auth import Authenticator

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))
    authenticator = Authenticator()
    is_allowed = authenticator.has_role("test_id")

    if is_allowed:
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': 'Hello, CDK! You have hit {}\n'.format(event['path'])
        }

    else:
        return {
            'statusCode': 403,
            'headers': {
                'Content-Type': 'text/plain'
            },
            'body': 'You are not authorized!'
        }
