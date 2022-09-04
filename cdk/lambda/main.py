import json
from auth import Authenticator, Role

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))
    user_id = "test_id"
    authenticator = Authenticator(user_id)
    is_allowed = authenticator.authenticate(Role.User.value)
    print(Role.User.value)

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
