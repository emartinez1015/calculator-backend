import os
import time
from cognitojwt import decode
from chalicelib.config import (COGNITO_CLIENT_ID, USER_POOL_ID, USER_POOL_REGION, 
                                LIVE_ARN_RESOURCES, LOCAL_ARN_RESOURCES)


class CognitoAuthSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        """
        Get the singleton instance of CognitoAuthSingleton class.

        Returns:
            CognitoAuthSingleton: The singleton instance.
        """
        if not CognitoAuthSingleton._instance:
            CognitoAuthSingleton._instance = CognitoAuthSingleton()
        return CognitoAuthSingleton._instance

    def __init__(self):
        """
        Initialize the CognitoAuthSingleton class.
        """
        if CognitoAuthSingleton._instance:
            raise Exception("This class is a singleton!")
        CognitoAuthSingleton._instance = self

    def authenticate_request(self, auth_request):
        """
        Authenticate the request using the provided authentication request.

        Args:
            auth_request (AuthRequest): The authentication request.

        Returns:
            dict: The policy document.

        Raises:
            Exception: If the token is expired or the issuer is invalid.
        """
        token = auth_request.token.replace('Bearer ', '')
        try:
            decoded_token = self._decode_token(token)
            self._validate_token(decoded_token)

            principal_id = decoded_token['sub']
            policy_document = self._generate_policy_document(principal_id, decoded_token)
            return policy_document

        except Exception as e:
            return {"message": str(e)}

    def _decode_token(self, token):
        """
        Decode the provided token.

        Args:
            token (str): The token to decode.

        Returns:
            dict: The decoded token.
        """
        return decode(
            token=token,
            region=USER_POOL_REGION,
            userpool_id=USER_POOL_ID,
            app_client_id=COGNITO_CLIENT_ID
        )

    def _validate_token(self, decoded_token):
        """
        Validate the decoded token.

        Args:
            decoded_token (dict): The decoded token.

        Raises:
            Exception: If the token is expired or the issuer is invalid.
        """
        if decoded_token['exp'] < time.time():
            raise Exception('Token has expired')

        expected_issuer = f'https://cognito-idp.{USER_POOL_REGION}.amazonaws.com/{USER_POOL_ID}'
        if decoded_token['iss'] != expected_issuer:
            raise Exception('Token issuer is invalid')

    def _generate_policy_document(self, principal_id, decoded_token):
        """
        Generate the policy document.

        Args:
            principal_id (str): The principal ID.
            decoded_token (dict): The decoded token.

        Returns:
            dict: The policy document.
        """
        resource_list = LIVE_ARN_RESOURCES + LOCAL_ARN_RESOURCES
        policy_document = {
            'principalId': principal_id,
            'context': decoded_token,
            'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Action': 'execute-api:Invoke',
                        'Effect': 'Allow',
                        'Resource': resource_list
                    }
                ]
            }
        }
        return policy_document
