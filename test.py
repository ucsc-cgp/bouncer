import unittest
import uuid
import boto3
import json

from bouncer import Bouncer, SecretManagerException

client = boto3.client('secretsmanager')


class TestBouncer(unittest.TestCase):
    good_secret_id = 'bouncer/test/secret/good/{}'.format(str(uuid.uuid4()).replace('-', ''))
    bad_secret_id = 'bouncer/test/secret/bad/{}'.format(str(uuid.uuid4()).replace('-', ''))

    @classmethod
    def setUpClass(cls):
        client.create_secret(
            Name=cls.good_secret_id,
            Description='test secret for bouncer. If this has been lying around '
                        'for any reasonable length of time then test cleanup is '
                        'probably not working properly',
            SecretString=json.dumps({'email': 'whitelisted@example.com,alsogood@example.com,metoo@example.com'}),
        )
        client.create_secret(
            Name=cls.bad_secret_id,
            Description='test secret for bouncer. If this has been lying around '
                        'for any reasonable length of time then test cleanup is '
                        'probably not working properly',
            SecretString=json.dumps({'emailZZZ': 'whitelisted@example.com,alsogood@example.com,metoo@example.com'}),
        )

    def test_valid_secret_name(self):
        """Tests the happy path"""
        bouncer = Bouncer(self.good_secret_id)
        self.assertTrue(bouncer.is_authorized('whitelisted@example.com'))
        self.assertTrue(bouncer.is_authorized('alsogood@example.com'))

    def test_invalid_secret_name(self):
        """We use a uuid to ensure this secret doesn't already exist"""
        bouncer = Bouncer('not/a/real/secret/{}'.format(str(uuid.uuid4()).replace('-', '')))
        self.assertRaises(SecretManagerException, bouncer.is_authorized, 'whitelisted@example.com', )

    def test_unauthorized_email(self):
        """Make sure an email that isn't on the whitelist won't be approved"""
        bouncer = Bouncer('commons/dev/whitelist')
        self.assertFalse(bouncer.is_authorized('notwhitelisted@example.com'))

    def test_invalid_secret_key(self):
        """
        This secret has the key `emailZZZ` instead of `email` so we want be sure that an error
        is raised as expected.
        """
        bouncer = Bouncer(self.bad_secret_id)
        self.assertRaises(SecretManagerException, bouncer.is_authorized, 'whitelisted@example.com', )

    @classmethod
    def tearDownClass(cls):
        client.delete_secret(SecretId=cls.good_secret_id)
