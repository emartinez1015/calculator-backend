import os
from cognitojwt import decode
import time


def cognito_auth(auth_request):
    token = auth_request.token.replace('Bearer ', '')

    # Validate the token using the cognitojwt library
    user_pool_region = os.environ['USER_POOL_REGION']
    user_pool_id = os.environ['USER_POOL_ID']
    app_client_id = os.environ['COGNITO_CLIENT_ID']

    try:
        decoded_token = decode(
            token=token,
            region=user_pool_region,
            userpool_id=user_pool_id,
            app_client_id=app_client_id
        )

        # Validate the token claims
        if decoded_token['exp'] < time.time():
            raise Exception('Token has expired')

        if decoded_token['iss'] != f'https://cognito-idp.{user_pool_region}.amazonaws.com/{user_pool_id}':
            raise Exception('Token issuer is invalid')

        # Token is valid, return the decoded token or required claims
        principal_id = decoded_token['sub']
        policy_document = {
            'principalId': principal_id,
            'context': decoded_token,
            'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Action': 'execute-api:Invoke',
                        'Effect': 'Allow',
                        'Resource': [
                            'arn:aws:execute-api:us-east-2:583847475803:ky23idqdol/*/GET/v1/operations',
                            'arn:aws:execute-api:us-east-2:583847475803:ky23idqdol/*/POST/v1/records',
                            'arn:aws:execute-api:us-east-2:583847475803:ky23idqdol/*/GET/v1/records',
                            'arn:aws:execute-api:us-east-2:583847475803:ky23idqdol/*/DELETE/v1/records/*',
                            'arn:aws:execute-api:us-east-2:583847475803:ky23idqdol/*/POST/v1/signout',
                            'arn:aws:execute-api:us-east-2:583847475803:ky23idqdol/*/GET/v1/random-string'
                        ]
                    }
                ]
            }
        }
        return policy_document

    except Exception as e:
        print(e)
        return {"message": str(e)}
