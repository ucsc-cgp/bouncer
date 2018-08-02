import unittest

from bouncer import Bouncer, SecretManagerException


class TestBouncer(unittest.TestCase):

    def setUp(self):
        pass

    def test_valid_secret_name(self):
        bouncer = Bouncer('commons/dev/whitelist')
        self.assertTrue(bouncer.is_authorized('donotdelete@testemail.com'))

    def test_invalid_secret_name(self):
        bouncer = Bouncer('jeeze/oh/pete/i/hope/no/one/actually/would/use/this/as/a/secret/name')
        self.assertRaises(SecretManagerException, bouncer.is_authorized, 'donotdelete@testemail.com', )

    def test_unauthorized_email(self):
        bouncer = Bouncer('commons/dev/whitelist')
        self.assertFalse(bouncer.is_authorized('this.email.address.will.not.be.in.whitelist@foo.bar'))
