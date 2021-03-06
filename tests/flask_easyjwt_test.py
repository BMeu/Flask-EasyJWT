#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch

from datetime import datetime
from datetime import timedelta

from flask import Flask

from flask_easyjwt import EasyJWTError
from flask_easyjwt import FlaskEasyJWT
from flask_easyjwt import InvalidSignatureError


# noinspection DuplicatedCode
class FlaskEasyJWTTest(TestCase):

    # region Test Setup

    def setUp(self):
        """
            Prepare the test cases.
        """

        self.easyjwt_key = 'abcdefghijklmnopqrstuvwxyz'
        self.secret_key = self.easyjwt_key[::-1]
        self.validity = 15  # In minutes.

        self.app = Flask(__name__)
        self.app.config['EASYJWT_KEY'] = self.easyjwt_key
        self.app.config['SECRET_KEY'] = self.secret_key

        self.custom_validity = self.validity + 15  # In minutes.
        self.custom_key = self.easyjwt_key + self.secret_key

        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """
            Clean up after each test case.
        """

        self.app_context.pop()

    # endregion

    # region Initialization

    def test_init_custom_key(self):
        """
            Test the initialization of the Flask-EasyJWT token with a custom key.

            Expected Result: The token object uses the user's key.
        """

        easyjwt = FlaskEasyJWT(self.custom_key)
        self.assertIsNotNone(easyjwt)
        self.assertEqual(self.custom_key, easyjwt._key)

    def test_init_default_key(self):
        """
            Test the initialization of the Flask-EasyJWT token with the default key from the extension.

            Expected Result: The token object uses the extension's key.
        """

        easyjwt = FlaskEasyJWT()
        self.assertIsNotNone(easyjwt)
        self.assertEqual(self.easyjwt_key, easyjwt._key)

    # endregion

    # region Creation

    def test_create_custom_expiration_date(self):
        """
            Test creating a token with a custom expiration date.

            Expected Result: The token object uses the user's expiration date.
        """

        self.app.config['EASYJWT_TOKEN_VALIDITY'] = timedelta(minutes=self.validity)
        expiration_date = datetime.utcnow().replace(microsecond=0) + timedelta(minutes=self.custom_validity)

        easyjwt = FlaskEasyJWT()
        easyjwt.expiration_date = expiration_date
        token = easyjwt.create()

        # After the creation, the expiration date is still the same.
        self.assertIsNotNone(token)
        self.assertEqual(expiration_date, easyjwt.expiration_date)

        # The verified token has the same expiration date.
        verified_easyjwt = FlaskEasyJWT.verify(token)
        self.assertIsNotNone(verified_easyjwt)
        self.assertEqual(expiration_date, verified_easyjwt.expiration_date)

    def test_create_default_expiration_date(self):
        """
            Test creating a token with the default expiration date.

            Expected Result: The token object uses the extension's expiration date.
        """

        self.app.config['EASYJWT_TOKEN_VALIDITY'] = timedelta(minutes=self.validity)

        easyjwt = FlaskEasyJWT()
        token = easyjwt.create()

        # After the creation, the expiration date from the extension is used.
        self.assertIsNotNone(token)
        self.assertIsNotNone(easyjwt.expiration_date)

        # The verified token has the same expiration date.
        verified_easyjwt = FlaskEasyJWT.verify(token)
        self.assertIsNotNone(verified_easyjwt)
        self.assertEqual(easyjwt.expiration_date, verified_easyjwt.expiration_date)

    # endregion

    # region Verification

    def test_verify_custom_key(self):
        """
            Test verifying a token created with a custom key.

            Expected Result: The token can be verified with the custom key, but not with the extension's key.
        """

        easyjwt = FlaskEasyJWT(self.custom_key)
        token = easyjwt.create()

        with self.assertRaises(InvalidSignatureError):
            verified_easyjwt = FlaskEasyJWT.verify(token)
            self.assertIsNone(verified_easyjwt)

        verified_easyjwt = FlaskEasyJWT.verify(token, self.custom_key)
        self.assertIsNotNone(verified_easyjwt)

    def test_verify_default_key(self):
        """
            Test verifying a token created with the default key.

            Expected Result: The token can be verified with the extension's key, but not with the custom key.
        """

        easyjwt = FlaskEasyJWT()
        token = easyjwt.create()

        with self.assertRaises(InvalidSignatureError):
            verified_easyjwt = FlaskEasyJWT.verify(token, self.custom_key)
            self.assertIsNone(verified_easyjwt)

        verified_easyjwt = FlaskEasyJWT.verify(token)
        self.assertIsNotNone(verified_easyjwt)

    # endregion

    # region Configuration Values

    @patch('flask_easyjwt.flask_easyjwt.warn')
    def test_get_validity_timedelta(self, mock_warn: MagicMock):
        """
            Test getting the validity if it is configured as a `timedelta` object.

            Expected Result: The token's validity as defined in the configuration. No warning is issued.
        """

        self.app.config['EASYJWT_TOKEN_VALIDITY'] = timedelta(minutes=self.validity)

        validity = FlaskEasyJWT.get_validity()
        self.assertEqual(self.app.config['EASYJWT_TOKEN_VALIDITY'], validity)
        mock_warn.assert_not_called()

    @patch('flask_easyjwt.flask_easyjwt.warn')
    def test_get_validity_integer(self, mock_warn: MagicMock):
        """
            Test getting the validity if it is configured as an integer.

            Expected Result: The token's validity as defined in the configuration. No warning is issued.
        """

        # The validity is interpreted in seconds when parsed from an integer.
        self.app.config['EASYJWT_TOKEN_VALIDITY'] = self.validity * 60

        validity = FlaskEasyJWT.get_validity()
        self.assertEqual(timedelta(seconds=self.app.config['EASYJWT_TOKEN_VALIDITY']), validity)
        mock_warn.assert_not_called()

    @patch('flask_easyjwt.flask_easyjwt.warn')
    def test_get_validity_no_app(self, mock_warn: MagicMock):
        """
            Test getting the validity if called outside an app context.

            Expected Result: A runtime error is thrown.
        """

        self.app_context.pop()
        with self.assertRaises(RuntimeError) as exception_cm:
            validity = FlaskEasyJWT.get_validity()
            self.assertIsNone(validity)

        message = 'Working outside of application context.'
        self.assertIn(message, str(exception_cm.exception))
        mock_warn.assert_not_called()

        # Push the app context again so that the tear down method will have something to pop.
        self.app_context.push()

    @patch('flask_easyjwt.flask_easyjwt.warn')
    def test_get_validity_none(self, mock_warn: MagicMock):
        """
            Test getting the validity if none is set in the configuration.

            Expected Result: `None` is returned. No warning is issued.
        """

        with self.assertRaises(KeyError):
            self.assertIsNone(self.app.config['EASYJWT_TOKEN_VALIDITY'])

        self.assertIsNone(FlaskEasyJWT.get_validity())
        mock_warn.assert_not_called()

    @patch('flask_easyjwt.flask_easyjwt.warn')
    def test_get_validity_string_parsable(self, mock_warn: MagicMock):
        """
            Test getting the validity if it is configured as a string that can be parsed to an integer.

            Expected Result: The token's validity as defined in the configuration. No warning is issued.
        """

        # The validity is interpreted in seconds when parsed from a string.
        self.app.config['EASYJWT_TOKEN_VALIDITY'] = str(self.validity * 60)

        validity = FlaskEasyJWT.get_validity()
        self.assertEqual(timedelta(seconds=int(self.app.config['EASYJWT_TOKEN_VALIDITY'])), validity)
        mock_warn.assert_not_called()

    @patch('flask_easyjwt.flask_easyjwt.warn')
    def test_get_config_expiration_date_string_unparsable(self, mock_warn: MagicMock):
        """
            Test getting the validity if it is configured as a string that cannot be parsed to an integer.

            Expected Result: `None` is returned. A warning is issued.
        """

        self.app.config['EASYJWT_TOKEN_VALIDITY'] = '15 minutes'

        expiration_date = FlaskEasyJWT.get_validity()
        self.assertIsNone(expiration_date)
        mock_warn.assert_called_once()

        warning = 'must be an int, a string castable to an int, or a datetime.timedelta'
        self.assertIn(warning, mock_warn.call_args_list[0][0][0])

    def test_get_expiration_date_no_validity(self):
        """
            Test getting the expiration date if no validity is defined in the application's configuration.

            Expected Result: `None` is returned.
        """

        with self.assertRaises(KeyError):
            self.assertIsNone(self.app.config['EASYJWT_TOKEN_VALIDITY'])

        self.assertIsNone(FlaskEasyJWT._get_config_expiration_date())

    def test_get_expiration_date_validity(self):
        """
            Test getting the expiration date if the validity is set in the application's configuration.

            Expected Result: The expiration date is the defined amount of time from now.
        """

        validity = timedelta(minutes=self.validity)
        self.app.config['EASYJWT_TOKEN_VALIDITY'] = validity

        # The returned expiration date is 15 minutes from now. To check the date, get the current time plus 15 minutes,
        # and get the time plus 15 minutes after getting the expiration date. The expiration date should then be between
        # those two times.
        lower_bound = datetime.utcnow().replace(microsecond=0) + validity
        expiration_date = FlaskEasyJWT._get_config_expiration_date()
        upper_bound = datetime.utcnow().replace(microsecond=0) + validity

        self.assertIsNotNone(expiration_date)
        self.assertGreaterEqual(expiration_date, lower_bound)
        self.assertLessEqual(expiration_date, upper_bound)

    def test_get_config_key_easyjwt(self):
        """
            Test getting the key from the EASYJWT_KEY configuration key.

            Expected Result: The EasyJWT key is returned.
        """

        key = FlaskEasyJWT._get_config_key()

        self.assertEqual(self.easyjwt_key, key)

    def test_get_config_key_no_app(self):
        """
            Test getting the key if called outside an app context.

            Expected Result: A runtime error is thrown.
        """

        self.app_context.pop()
        with self.assertRaises(RuntimeError) as exception_cm:
            key = FlaskEasyJWT._get_config_key()
            self.assertIsNone(key)

        message = 'Working outside of application context.'
        self.assertIn(message, str(exception_cm.exception))

        # Push the app context again so that the tear down method will have something to pop.
        self.app_context.push()

    def test_get_config_key_none(self):
        """
            Test getting the key if none is set.

            Expected Result: An error is raised.
        """

        del self.app.config['EASYJWT_KEY']
        del self.app.config['SECRET_KEY']

        with self.assertRaises(EasyJWTError) as exception_cm:
            key = FlaskEasyJWT._get_config_key()
            self.assertIsNone(key)

        message = 'No key set for encrypting tokens.'
        self.assertIn(message, str(exception_cm.exception))

    def test_get_config_key_secret(self):
        """
            Test getting the key from the SECRET_KEY configuration key if EASYJWT_KEY is not configured.

            Expected Result: The secret key is returned.
        """

        del self.app.config['EASYJWT_KEY']

        key = FlaskEasyJWT._get_config_key()

        self.assertEqual(self.secret_key, key)

    # endregion
