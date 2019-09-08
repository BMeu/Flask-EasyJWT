#!/usr/bin/python
# -*- coding: utf-8 -*-

from unittest import TestCase

from datetime import timedelta

from flask import Flask

from easyjwt import EasyJWTError
from flask_easyjwt import FlaskEasyJWT


class AccountValidationToken(FlaskEasyJWT):

    def __init__(self, key=None):
        super().__init__(key)

        self.user_id = None


class IntegrationTest(TestCase):

    # region Flask App

    def _create_app(self) -> Flask:
        """
            Create a Flask test application.

            :return: The newly created application instance.
        """

        application = Flask(__name__)
        application.config.from_mapping(
            EASYJWT_KEY=self.easyjwt_key,
            EASYJWT_VALIDITY=self.validity,
            SECRET_KEY=self.secret_key,
        )

        application.add_url_rule('/get_token/<int:user_id>', view_func=self._get_token)
        application.add_url_rule('/validate_user/<string:token>', view_func=self._validate_user)

        return application

    @staticmethod
    def _get_token(user_id: int) -> str:
        """
            Get an account validation token.

            :param user_id: The value of the `user_id` claim.
            :return: The created token.
        """

        token = AccountValidationToken()
        token.user_id = user_id

        return token.create()

    @staticmethod
    def _validate_user(token: str):
        """
            Verify the user given in the given account validation token.

            :param token: A JWT created with :class:`AccountValidationToken`.
            :return: The user ID of the validated user on success, 0 on failure - both as a string.
        """

        try:
            token = AccountValidationToken.verify(token)
            user_id = token.user_id
        except EasyJWTError:
            user_id = 0

        return str(user_id)

    # endregion

    # region Test Setup

    def setUp(self):
        """
            Prepare the test cases.
        """

        self.easyjwt_key = 'abcdefghijklmnopqrstuvwxyz'
        self.secret_key = self.easyjwt_key[::-1]
        self.validity = timedelta(minutes=5)

        self.app = self._create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.request_context = self.app.test_request_context()
        self.request_context.push()

    def tearDown(self):
        """
            Clean up after each test case.
        """

        self.request_context.pop()
        self.app_context.pop()

    # endregion

    def test_validate_failure(self):
        """
            Test validating a token that is not valid.

            Expected Result: The token is rejected.
        """

        # Use a different key for creating the token then for validating it.
        token_object = AccountValidationToken(self.easyjwt_key[::-1])
        token_object.user_id = 42
        token = token_object.create()

        response = self.client.get(f'/validate_user/{token}')
        validated_user = response.get_data(as_text=True)
        self.assertEqual(str(0), validated_user)

    def test_validate_success(self):
        """
            Test getting and successfully validating a token.

            Expected Result: A token can be requested from the app and then successfully validated.
        """

        user_id = 42
        response = self.client.get(f'/get_token/{user_id}')
        token = response.get_data(as_text=True)
        self.assertIsNotNone(token)

        response = self.client.get(f'/validate_user/{token}')
        validated_user = response.get_data(as_text=True)
        self.assertEqual(str(user_id), validated_user)
