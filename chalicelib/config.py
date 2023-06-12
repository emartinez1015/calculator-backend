# config.py

import os

USER_POOL_REGION = os.environ.get('USER_POOL_REGION')
COGNITO_CLIENT_ID = os.environ.get('COGNITO_CLIENT_ID')
USER_POOL_ID = os.environ['USER_POOL_ID']
RAMDON_ORG_URL = 'https://www.random.org/strings/'

LIVE_ARN_RESOURCES = [
    'arn:aws:execute-api:us-east-2:583847475803:ky23idqdol/*/GET/v1/operations',
    'arn:aws:execute-api:us-east-2:583847475803:ky23idqdol/*/POST/v1/records',
    'arn:aws:execute-api:us-east-2:583847475803:ky23idqdol/*/GET/v1/records',
    'arn:aws:execute-api:us-east-2:583847475803:ky23idqdol/*/DELETE/v1/records/*',
    'arn:aws:execute-api:us-east-2:583847475803:ky23idqdol/*/POST/v1/signout',
    'arn:aws:execute-api:us-east-2:583847475803:ky23idqdol/*/GET/v1/random-string'
]

LOCAL_ARN_RESOURCES = [
    'arn:aws:execute-api:mars-west-1:123456789012:ymy8tbxw7b/*/GET/v1/operations',
    'arn:aws:execute-api:mars-west-1:123456789012:ymy8tbxw7b/*/POST/v1/records',
    'arn:aws:execute-api:mars-west-1:123456789012:ymy8tbxw7b/*/GET/v1/records',
    'arn:aws:execute-api:mars-west-1:123456789012:ymy8tbxw7b/*/DELETE/v1/records/*',
    'arn:aws:execute-api:mars-west-1:123456789012:ymy8tbxw7b/*/POST/v1/signout',
    'arn:aws:execute-api:mars-west-1:123456789012:ymy8tbxw7b/*/GET/v1/random-string'
]