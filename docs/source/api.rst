API
===

.. automodule:: flask_easyjwt

.. contents:: Contents
    :backlinks: none
    :local:

Classes
-------

This section lists all classes defined by |project|.

.. autoclass:: flask_easyjwt.FlaskEasyJWT
    :inherited-members:
    :members:
    :show-inheritance:

Enumerations
------------

This section lists all enumerations defined by |project|.

.. autoclass:: flask_easyjwt.Algorithm
    :members:
    :show-inheritance:

Errors
------

This section lists all error classes defined by |project|.

.. autoexception:: flask_easyjwt.EasyJWTError
    :members:
    :show-inheritance:

Creation Errors
~~~~~~~~~~~~~~~

This section lists all error classed defined by |project| that may be raised during the creation of a token. Note that
some error classes may also listed below `Verification Errors`_.

.. autoexception:: flask_easyjwt.CreationError
    :members:
    :show-inheritance:

.. autoexception:: flask_easyjwt.IncompatibleKeyError
    :members:
    :show-inheritance:

.. autoexception:: flask_easyjwt.MissingRequiredClaimsError
    :members:
    :show-inheritance:

Verification Errors
~~~~~~~~~~~~~~~~~~~

This section lists all error classed defined by |project| that may be raised during the verification of a token. Note
that some error classes may also listed below `Creation Errors`_.

.. autoexception:: flask_easyjwt.VerificationError
    :members:
    :show-inheritance:

.. autoexception:: flask_easyjwt.ExpiredTokenError
    :members:
    :show-inheritance:

.. autoexception:: flask_easyjwt.ImmatureTokenError
    :members:
    :show-inheritance:

.. autoexception:: flask_easyjwt.IncompatibleKeyError
    :members:
    :show-inheritance:

.. autoexception:: flask_easyjwt.InvalidAudienceError
    :members:
    :show-inheritance:

.. autoexception:: flask_easyjwt.InvalidClaimSetError
    :members:
    :show-inheritance:

.. autoexception:: flask_easyjwt.InvalidClassError
    :members:
    :show-inheritance:

.. autoexception:: flask_easyjwt.InvalidIssuedAtError
    :members:
    :show-inheritance:

.. autoexception:: flask_easyjwt.InvalidIssuerError
    :members:
    :show-inheritance:

.. autoexception:: flask_easyjwt.InvalidSignatureError
    :members:
    :show-inheritance:

.. autoexception:: flask_easyjwt.UnspecifiedClassError
    :members:
    :show-inheritance:

.. autoexception:: flask_easyjwt.UnsupportedAlgorithmError
    :members:
    :show-inheritance:

Types
-----

This section lists the types defined by |project|.

.. autodata:: flask_easyjwt.flask_easyjwt.FlaskEasyJWTClass
