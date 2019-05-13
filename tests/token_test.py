#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import MagicMock

from datetime import datetime
from datetime import timedelta

from easyjwt import InvalidSignatureError

from flask_easyjwt import Token


class TokenTest(TestCase):

    # region Test Setup

    def setUp(self):
        """
            Prepare the test cases.
        """

        # Create values for the expiration date and key to be used in the "extension".
        self.extension_expiration_date = datetime.utcnow().replace(microsecond=0) + timedelta(minutes=15)
        self.extension_key = 'abcdefghijklmnopqrstuvwxyz'

        # Create an expiration date and key that are definitively different to the ones in the "extension".
        self.custom_expiration_date = self.extension_expiration_date + timedelta(minutes=15)
        self.custom_key = self.extension_key[::-1]

        # Create a fake extension.
        self.mock_extension = MagicMock()
        self.mock_extension.expiration_date = self.extension_expiration_date
        self.mock_extension.key = self.extension_key

        # Set the extension on the token class.
        Token.flask_easyjwt = self.mock_extension

    def tearDown(self):
        """
            Clean up after each test case.
        """

        # Reset the extension.
        Token.flask_easyjwt = None

    # endregion

    def test_init_custom_key(self):
        """
            Test the initialization of the Flask-EasyJWT token with a custom key.

            Expected Result: The token object uses the user's key.
        """

        token_object = Token(self.custom_key)
        self.assertIsNotNone(token_object)
        self.assertEqual(self.custom_key, token_object._key)

    def test_init_default_key(self):
        """
            Test the initialization of the Flask-EasyJWT token with the default key from the extension.

            Expected Result: The token object uses the extension's key.
        """

        token_object = Token()
        self.assertIsNotNone(token_object)
        self.assertEqual(self.extension_key, token_object._key)

    def test_create_custom_expiration_date(self):
        """
            Test creating a token with a custom expiration date.

            Expected Result: The token object uses the user's expiration date.
        """

        token_object = Token()
        token_object.expiration_date = self.custom_expiration_date
        token = token_object.create()

        # After the creation, the expiration date is still the same.
        self.assertIsNotNone(token)
        self.assertEqual(self.custom_expiration_date, token_object.expiration_date)

        # The verified token has the same expiration date.
        verified_token_object = Token.verify(token)
        self.assertIsNotNone(verified_token_object)
        self.assertEqual(self.custom_expiration_date, verified_token_object.expiration_date)

    def test_create_default_expiration_date(self):
        """
            Test creating a token with the default expiration date.

            Expected Result: The token object uses the extension's expiration date.
        """

        token_object = Token()
        token = token_object.create()

        # After the creation, the expiration date from the extension is used.
        self.assertIsNotNone(token)
        self.assertEqual(self.extension_expiration_date, token_object.expiration_date)

        # The verified token has the same expiration date.
        verified_token_object = Token.verify(token)
        self.assertIsNotNone(verified_token_object)
        self.assertEqual(self.extension_expiration_date, verified_token_object.expiration_date)

    def test_verify_custom_key(self):
        """
            Test verify a token created with a custom key.

            Expected Result: The token can be verified with the custom key, but not with the extension's key.
        """

        token_object = Token(self.custom_key)
        token = token_object.create()

        with self.assertRaises(InvalidSignatureError):
            verified_token_object = Token.verify(token)
            self.assertIsNone(verified_token_object)

        verified_token_object = Token.verify(token, self.custom_key)
        self.assertIsNotNone(verified_token_object)

    def test_verify_default_key(self):
        """
            Test verify a token created with the default key.

            Expected Result: The token can be verified with the extension's key, but not with the custom key.
        """

        token_object = Token()
        token = token_object.create()

        with self.assertRaises(InvalidSignatureError):
            verified_token_object = Token.verify(token, self.custom_key)
            self.assertIsNone(verified_token_object)

        verified_token_object = Token.verify(token)
        self.assertIsNotNone(verified_token_object)
