
import json

import boto3
from botocore.exceptions import ClientError


SECRETS_MANAGER_URL = "https://secretsmanager.us-west-2.amazonaws.com"
SECRET_KEY = 'email'


class SecretManagerException(Exception):
    pass


class Bouncer(object):
    """
    Client convenience class to perform email whitelist authorization
    """
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', endpoint_url=SECRETS_MANAGER_URL)

    def __init__(self, secret_name: str):
        """
        :param secret_name: The name of the secret in
        the AWS Secret Manager. For example: commons/dev/whitelist
        """
        self.secret_name = secret_name

    def is_authorized(self, email: str) -> bool:
        """
        Identify if the given email address is included in the email whitelist.

        :param email: Google email address for which authorization is to be determined
        :return: True if the email address is authorized, False if not authorized
        :exception SecretManagerException: If an error occurs.
        """
        return email in self.whitelist()

    def whitelist(self):
        try:
            get_secret_value_response = self.client.get_secret_value(SecretId=self.secret_name)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                raise SecretManagerException("The requested secret " + self.secret_name + " was not found") from e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                raise SecretManagerException("The request was invalid due to:", e) from e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                raise SecretManagerException("The request had invalid params:", e) from e
        else:
            secret_string = get_secret_value_response['SecretString']
            secret_dict = json.loads(secret_string)
            try:
                return secret_dict[SECRET_KEY].split(',')
            except KeyError as e:
                raise SecretManagerException(f"Your secret is misformatted. Expected key: {SECRET_KEY}, "
                                             f"actually found: {list(secret_dict.keys())}")
