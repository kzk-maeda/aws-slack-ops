import json
import auth as auth

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))
    auth.handler("test")

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': 'Hello, CDK! You have hit {}\n'.format(event['path'])
    }
