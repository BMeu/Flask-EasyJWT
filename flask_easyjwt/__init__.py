#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Flask-EasyJWT provides a simple interface to creating and verifying
    `JSON Web Tokens (JWTs) <https://tools.ietf.org/html/rfc7519>`_ in Python. It allows you to once define the claims
    of the JWT, and to then create and accept tokens with these claims without having to check if all the required data
    is given or if the token actually is the one you expect.

    Flask-EasyJWT is a simple wrapper around `EasyJWT <https://github.com/BMeu/EasyJWT>`_ for easy usage in
    `Flask <http://flask.pocoo.org/>`_ applications. It provides configuration options via Flask's application
    configuration  for common settings of all tokens created in a web application.

    See the included README file or the `documentation <https://flask-easyjwt.readthedocs.io/en/latest/index.html>`_ for
    details on how to use Flask-EasyJWT.
"""

from .flask_easyjwt import FlaskEasyJWT
from .token import Token

__all__ = [
    'FlaskEasyJWT',
    'Token',
]
