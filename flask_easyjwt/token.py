#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Definition of the actual token base class.
"""

from typing import ClassVar
from typing import Iterable
from typing import Optional
from typing import Type
from typing import Union

from datetime import datetime

from easyjwt import EasyJWT
from easyjwt import EasyJWTClass

from flask_easyjwt import FlaskEasyJWT


class Token(EasyJWT):
    """
        The base class for representing JSON Web Tokens.

        To define tokens, subclass :attr:`flask_easyjwt.Token <FlaskEasyJWT.Token>`, not this class. To customize
        :attr:`flask_easyjwt.Token <FlaskEasyJWT.Token>`, subclass this class and pass it as `token_class` to
        :class:`FlaskEasyJWT`.
    """

    flask_easyjwt: ClassVar[FlaskEasyJWT] = None
    """
        The :class:`FlaskEasyJWT` extension instance.
    """

    def __init__(self, key: Optional[str] = None) -> None:
        """
            :param key: If set, the given string will be used to encrypt tokens when they are created. If not given,
                        the key defined in the application's configuration will be used. Defaults to `None`.
        """
        if key is None:
            key = self.flask_easyjwt.key

        # Perform the default initialization with the chosen key.
        super().__init__(key)

    def create(self, issued_at: Optional[datetime] = None) -> str:
        """
            Create the actual token from the :class:`EasyJWT` object. Empty optional claims will not be included in the
            token. Empty non-optional claims will cause a :class:`MissingRequiredClaimsError`.

            :param issued_at: The date and time at which this token was issued. If not given, the current date and time
                              will be used. Must be given in UTC. Defaults to `None`.
            :return: The token represented by the current state of the object.
            :raise IncompatibleKeyError: If the given key is incompatible with the algorithm used for encoding the
                                         token.
            :raise MissingRequiredClaimsError: If instance variables that map to non-optional claims in the claim set
                                               are empty.
        """

        # If the expiration date is not set, set it from the application's configuration.
        if self.expiration_date is None:
            self.expiration_date = self.flask_easyjwt.expiration_date

        return super().create(issued_at)

    @classmethod
    def verify(cls: Type['Token'],
               token: str,
               key: Optional[str] = None,
               issuer: Optional[str] = None,
               audience: Optional[Union[Iterable[str], str]] = None
               ) -> EasyJWTClass:
        """
            Verify the given JSON Web Token.

            :param token: The JWT to verify.
            :param key: The key used for decoding the token. This key must be the same with which the token has been
                        created.
            :param issuer: The issuer of the token to verify.
            :param audience: The audience for which the token is intended.
            :return: The object representing the token. The claim values are set on the corresponding instance
                     variables.
            :raise ExpiredTokenError: If the claim set contains an expiration date claim ``exp`` that has passed.
            :raise ImmatureTokenError: If the claim set contains a not-before date claim ``nbf`` that has not yet been
                                       reached.
            :raise IncompatibleKeyError: If the given key is incompatible with the algorithm used for decoding the
                                         token.
            :raise InvalidAudienceError: If the given audience is not specified in the token's audience claim, or no
                                         audience is given when verifying a token with an audience claim, or the given
                                         audience is not a string, an iterable, or `None`.
            :raise InvalidClaimSetError: If the claim set does not contain exactly the expected (non-optional) claims.
            :raise InvalidClassError: If the claim set is not verified with the class with which the token has been
                                      created.
            :raise InvalidIssuedAtError: If the claim set contains an issued-at date ``iat`` that is not an integer.
            :raise InvalidIssuerError: If the token has been issued by a different issuer than given.
            :raise InvalidSignatureError: If the token's signature does not validate the token's contents.
            :raise UnspecifiedClassError: If the claim set does not contain the class with which the token has been
                                          created.
            :raise UnsupportedAlgorithmError: If the algorithm used for encoding the token is not supported.
            :raise VerificationError: If a general error occurred during decoding.
        """

        if key is None:
            key = cls.flask_easyjwt.key

        return super().verify(token, key, issuer, audience)
