#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Definition of the actual Flask extension.
"""

from typing import Optional

from datetime import datetime
from datetime import timedelta
from warnings import warn

from flask import current_app
from flask import Flask


_CONFIGURATION_KEY = 'EASYJWT_KEY'
"""
    The name of the configuration key for the encryption key.
"""

_CONFIGURATION_TOKEN_VALIDITY = 'EASYJWT_TOKEN_VALIDITY'
"""
    The name of the configuration key for the token's validity.
"""


class FlaskEasyJWT(object):
    """
        The extension class for the usage of `EasyJWT` with `Flask`.

        You can either initialize this extension by passing your `Flask` application instance to the constructor, or
        by passing it to :meth:`.init_app` in a factory method.
    """

    # region Attributes & Properties

    @property
    def _application(self) -> Flask:
        """
            Get the Flask application to be used for accessing the configuration.

            :return: If set, the application with which this extension has been initialized in the constructor.
                     Otherwise, the current application.
        """

        if self._explicit_application is not None:
            return self._explicit_application

        return current_app

    @property
    def expiration_date(self) -> Optional[datetime]:
        """
            Get the expiration date, based on the tokens' validity defined in the application's configuration.

            :return: None if no token validity is defined in the application's configuration or if the value has a wrong
                     type. A `datetime` object otherwise, in UTC and the defined amount of time from now.
        """

        # If no token validity is defined, the token won't have an expiration date.
        validity = self._application.config[_CONFIGURATION_TOKEN_VALIDITY]
        if validity is None:
            return None

        # If the validity is specified as a string, convert it to an integer.
        if isinstance(validity, str):
            try:
                validity = int(validity)
            except ValueError:
                # If the string cannot be parsed to an integer, the validity is invalid.
                # In this case, let the validity as is; the following checks will fail as well,
                # and thus, a warning will be issued.
                pass

        # If the validity is specified as an integer or has been parsed to one, convert it to a timedelta object.
        if isinstance(validity, int):
            validity = timedelta(seconds=validity)

        # If the validity still is not a timedelta object, issue a warning.
        if not isinstance(validity, timedelta):
            warn(f'{_CONFIGURATION_TOKEN_VALIDITY} must be an int, a string castable to an int, or datetime.timedelta.')
            return None

        # The expiration date of the token is the given amount of time from now.
        return datetime.utcnow() + validity

    @property
    def key(self) -> Optional[str]:
        """
            Get the key for encrypting and decrypting tokens.

            If the application does not define a key, a warning will be issued.

            :return: The key defined in the application's configuration. `None` if none is set.
        """

        key = self._application.config[_CONFIGURATION_KEY]
        if key is None:
            warn(f'No key set, token will not be encrypted. Set {_CONFIGURATION_KEY}.')
            return None

        return key

    # endregion

    # region Initialization

    def __init__(self, application: Optional[Flask] = None) -> None:
        """
            :param application: Optionally, the application that will be initialized. The application can also later be
                                initialized with :meth:`.init_app`.
        """

        # Initialize the application if given.
        self._explicit_application = application
        if application is not None:
            self.init_app(application)

    def init_app(self, application: Flask) -> None:
        """
            Initialize the application for the use with Flask-EasyJWT.

            :param application: The application that will be initialized.
        """

        application.extensions['easyjwt'] = self

        # Fall back to the secret key of the application.
        configuration_secret_key = 'SECRET_KEY'
        secret_key = application.config.get(configuration_secret_key, None)

        # Set configuration defaults.
        application.config.setdefault(_CONFIGURATION_KEY, secret_key)
        application.config.setdefault(_CONFIGURATION_TOKEN_VALIDITY, None)

        # Warn if there is no key set.
        if application.config[_CONFIGURATION_KEY] is None:
            warn(f'No key set for encrypting tokens. Set {configuration_secret_key} or {_CONFIGURATION_KEY}.')

    # endregion
