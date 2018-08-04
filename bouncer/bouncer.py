import json
import boto3

import six
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

    def __init__(self, secret_name):
        """
        :param secret_name: The name of the secret in
        :type secret_name: str
        the AWS Secret Manager. For example: commons/dev/whitelist
        """
        self.secret_name = secret_name

    def is_authorized(self, email):
        """
        Identify if the given email address is included in the email whitelist.

        :param email: Google email address for which authorization is to be determined
        :type email: str
        :return: True if the email address is authorized, False if not authorized
        :exception SecretManagerException: If an error occurs.
        """
        return email in self.whitelist()

    def whitelist(self):
        try:
            get_secret_value_response = self.client.get_secret_value(SecretId=self.secret_name)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                six.raise_from(SecretManagerException("The requested secret {} was not found"
                                                      .format(self.secret_name)), e)
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                six.raise_from(SecretManagerException("The request was invalid due to:", e), e)
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                six.raise_from(SecretManagerException("The request had invalid params:", e), e)
            else:
                raise
        else:
            secret_string = get_secret_value_response['SecretString']
            secret_dict = json.loads(secret_string)
            try:
                return secret_dict[SECRET_KEY].split(',')
            except KeyError:
                raise SecretManagerException("Your secret is misformatted. Expected key: {}, actually found: {}"
                                             .format(SECRET_KEY, list(secret_dict.keys())))
