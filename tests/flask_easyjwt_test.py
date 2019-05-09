#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import patch

from datetime import datetime
from datetime import timedelta

from flask import Flask

from flask_easyjwt import FlaskEasyJWT


class FlaskEasyJWTTest(TestCase):

    # region Test Setup

    def setUp(self):
        """
            Prepare the test cases.
        """

        self.easyjwt_key = 'abcdefghijklmnopqrstuvwxyz'
        self.secret_key = self.easyjwt_key[::-1]

        self.app = Flask(__name__)
        self.app.config['EASYJWT_KEY'] = self.easyjwt_key
        self.app.config['SECRET_KEY'] = self.secret_key

    def tearDown(self):
        """
            Clean up after each test case.
        """
        pass

    # endregion

    # region Attributes & Properties

    def test_application_defined(self):
        """
            Test getting the application if it has been defined in the constructor.

            Expected Result: The set application is returned.
        """

        easyjwt = FlaskEasyJWT(self.app)
        app = easyjwt._application
        self.assertEqual(self.app, app)

    def test_application_undefined(self):
        """
            Test getting the application if it has not been defined in the constructor.

            Expected Result: The `current_app` is returned.
        """

        easyjwt = FlaskEasyJWT()
        with self.app.app_context():
            app = easyjwt._application
            self.assertEqual(self.app, app)

    @patch('flask_easyjwt.flask_easyjwt.warn')
    def test_expiration_date_timedelta(self, mock_warn: MagicMock):
        """
            Test getting the expiration date if the validity is configured as a `timedelta` object.

            Expected Result: The token's validity is the defined amount of time away from now. No warning is issued.
        """

        # Set the validity to 15 minutes.
        validity = 15
        self.app.config['EASYJWT_TOKEN_VALIDITY'] = timedelta(minutes=validity)

        easyjwt = FlaskEasyJWT(self.app)

        # The returned expiration date is 15 minutes from now. To check the date, get the current time plus 15 minutes,
        # and get the time plus 15 minutes after getting the expiration date. The expiration date should then be between
        # those two times.
        lower_bound = datetime.utcnow() + timedelta(minutes=validity)
        expiration_date = easyjwt.expiration_date
        upper_bound = datetime.utcnow() + timedelta(minutes=validity)

        self.assertIsNotNone(expiration_date)
        self.assertGreaterEqual(expiration_date, lower_bound)
        self.assertLessEqual(expiration_date, upper_bound)
        mock_warn.assert_not_called()

    @patch('flask_easyjwt.flask_easyjwt.warn')
    def test_expiration_date_integer(self, mock_warn: MagicMock):
        """
            Test getting the expiration date if the validity is configured as an integer.

            Expected Result: The token's validity is the defined amount of time away from now. No warning is issued.
        """

        # Set the validity to 15 minutes.
        validity = 15 * 60
        self.app.config['EASYJWT_TOKEN_VALIDITY'] = validity

        easyjwt = FlaskEasyJWT(self.app)

        # The returned expiration date is 15 minutes from now. To check the date, get the current time plus 15 minutes,
        # and get the time plus 15 minutes after getting the expiration date. The expiration date should then be between
        # those two times.
        lower_bound = datetime.utcnow() + timedelta(seconds=validity)
        expiration_date = easyjwt.expiration_date
        upper_bound = datetime.utcnow() + timedelta(seconds=validity)

        self.assertIsNotNone(expiration_date)
        self.assertGreaterEqual(expiration_date, lower_bound)
        self.assertLessEqual(expiration_date, upper_bound)
        mock_warn.assert_not_called()

    @patch('flask_easyjwt.flask_easyjwt.warn')
    def test_expiration_date_none(self, mock_warn: MagicMock):
        """
            Test getting the expiration date if none is set in the configuration.

            Expected Result: `None` is returned. No warning is issued.
        """

        easyjwt = FlaskEasyJWT(self.app)

        self.assertIsNone(self.app.config['EASYJWT_TOKEN_VALIDITY'])
        self.assertIsNone(easyjwt.expiration_date)
        mock_warn.assert_not_called()

    @patch('flask_easyjwt.flask_easyjwt.warn')
    def test_expiration_date_string_parsable(self, mock_warn: MagicMock):
        """
            Test getting the expiration date if the validity is configured as a string that can be parsed to an integer.

            Expected Result: The token's validity is the defined amount of time away from now. No warning is issued.
        """

        # Set the validity to 15 minutes.
        validity = 15 * 60
        self.app.config['EASYJWT_TOKEN_VALIDITY'] = str(validity)

        easyjwt = FlaskEasyJWT(self.app)

        # The returned expiration date is 15 minutes from now. To check the date, get the current time plus 15 minutes,
        # and get the time plus 15 minutes after getting the expiration date. The expiration date should then be between
        # those two times.
        lower_bound = datetime.utcnow() + timedelta(seconds=validity)
        expiration_date = easyjwt.expiration_date
        upper_bound = datetime.utcnow() + timedelta(seconds=validity)

        self.assertIsNotNone(expiration_date)
        self.assertGreaterEqual(expiration_date, lower_bound)
        self.assertLessEqual(expiration_date, upper_bound)
        mock_warn.assert_not_called()

    @patch('flask_easyjwt.flask_easyjwt.warn')
    def test_expiration_date_string_unparsable(self, mock_warn: MagicMock):
        """
            Test getting the expiration date if the validity is configured as a string that cannot be parsed to an
            integer.

            Expected Result: `None` is returned. A warning is issued.
        """

        self.app.config['EASYJWT_TOKEN_VALIDITY'] = '15 minutes'

        easyjwt = FlaskEasyJWT(self.app)
        expiration_date = easyjwt.expiration_date
        self.assertIsNone(expiration_date)
        mock_warn.assert_called_once()

        warning = 'must be an int, a string castable to an int, or datetime.timedelta'
        self.assertIn(warning, mock_warn.call_args_list[0][0][0])

    @patch('flask_easyjwt.flask_easyjwt.warn')
    def test_key_none(self, mock_warn: MagicMock):
        """
            Test getting the key if none is set.

            Expected Result: `None` is returned. A warning is issued.
        """

        del self.app.config['EASYJWT_KEY']
        del self.app.config['SECRET_KEY']

        easyjwt = FlaskEasyJWT(self.app)
        key = easyjwt.key

        self.assertIsNone(key)
        mock_warn.assert_called()
        self.assertEqual(2, mock_warn.call_count)

        warning = 'No key set, token will not be encrypted.'
        self.assertIn(warning, mock_warn.call_args_list[1][0][0])

    @patch('flask_easyjwt.flask_easyjwt.warn')
    def test_key_set(self, mock_warn: MagicMock):
        """
            Test getting the key if one is configured.

            Expected Result: The key is returned. No warning is issued.
        """

        easyjwt = FlaskEasyJWT(self.app)
        key = easyjwt.key

        self.assertEqual(self.easyjwt_key, key)
        mock_warn.assert_not_called()

    # endregion

    # region Initialization

    def test_init_with_app(self):
        """
            Test initializing the extension with giving an application.

            Expected Result: The extension is initialized. The application is saved. The application is initialized for
                             the extension.
        """

        easyjwt = FlaskEasyJWT(self.app)
        self.assertIsNotNone(easyjwt)
        self.assertEqual(self.app, easyjwt._explicit_application)
        self.assertEqual(self.app.extensions['easyjwt'], easyjwt)

    def test_init_without_app(self):
        """
            Test initializing the extension without giving an application.

            Expected Result: The extension is initialized. No application is saved.
        """

        easyjwt = FlaskEasyJWT()
        self.assertIsNotNone(easyjwt)
        self.assertIsNone(easyjwt._explicit_application)

    @patch('flask_easyjwt.flask_easyjwt.warn')
    def test_init_app_with_easyjwt_key(self, mock_warn: MagicMock):
        """
            Test initializing the application if the EASYJWT_KEY configuration is set.

            Expected Result: The application is initialized. No warning is issued.
        """

        easyjwt = FlaskEasyJWT()
        easyjwt.init_app(self.app)

        self.assertEqual(self.app.extensions['easyjwt'], easyjwt)
        self.assertEqual(self.easyjwt_key, self.app.config['EASYJWT_KEY'])
        self.assertIsNone(self.app.config['EASYJWT_TOKEN_VALIDITY'])
        mock_warn.assert_not_called()

    @patch('flask_easyjwt.flask_easyjwt.warn')
    def test_init_app_with_secret_key(self, mock_warn: MagicMock):
        """
            Test initializing the application if the EASYJWT_KEY configuration is not set, but the SECRET_KEY.

            Expected Result: The application is initialized. No warning is issued.
        """

        # Delete the EASYJWT_KEY from the configuration, so the default will be set to SECRET_KEY.
        del self.app.config['EASYJWT_KEY']
        with self.assertRaises(KeyError):
            self.assertIsNone(self.app.config['EASYJWT_KEY'])

        easyjwt = FlaskEasyJWT()
        easyjwt.init_app(self.app)

        self.assertEqual(self.app.extensions['easyjwt'], easyjwt)
        self.assertEqual(self.secret_key, self.app.config['EASYJWT_KEY'])
        self.assertIsNone(self.app.config['EASYJWT_TOKEN_VALIDITY'])
        mock_warn.assert_not_called()

    @patch('flask_easyjwt.flask_easyjwt.warn')
    def test_init_app_without_keys(self, mock_warn: MagicMock):
        """
            Test initializing the application if neither the EASYJWT_KEY configuration nor the SECRET_KEY one.

            Expected Result: The application is initialized. A warning is issued.
        """

        # Delete the EASYJWT_KEY from the configuration.
        del self.app.config['EASYJWT_KEY']
        with self.assertRaises(KeyError):
            self.assertIsNone(self.app.config['EASYJWT_KEY'])

        # Delete the SECRET_KEY from the configuration.
        del self.app.config['SECRET_KEY']
        with self.assertRaises(KeyError):
            self.assertIsNone(self.app.config['SECRET_KEY'])

        easyjwt = FlaskEasyJWT()
        easyjwt.init_app(self.app)

        self.assertEqual(self.app.extensions['easyjwt'], easyjwt)
        self.assertIsNone(self.app.config['EASYJWT_KEY'])
        self.assertIsNone(self.app.config['EASYJWT_TOKEN_VALIDITY'])
        mock_warn.assert_called_once()

        warning = 'No key set for encrypting tokens.'
        self.assertIn(warning, mock_warn.call_args_list[0][0][0])

    # endregion
