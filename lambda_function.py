import json

def lambda_handler(event, context):
    # Add your logic and route handler.

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
