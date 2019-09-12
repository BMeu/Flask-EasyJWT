# Flask-EasyJWT

[![Build Status](https://travis-ci.org/BMeu/Flask-EasyJWT.svg?branch=master)](https://travis-ci.org/BMeu/Flask-EasyJWT)
[![codecov](https://codecov.io/gh/BMeu/Flask-EasyJWT/branch/master/graph/badge.svg)](https://codecov.io/gh/BMeu/Flask-EasyJWT)
[![Documentation Status](https://readthedocs.org/projects/flask-easyjwt/badge/?version=latest)](https://flask-easyjwt.readthedocs.io/en/latest/?badge=latest)

Flask-EasyJWT provides a simple interface to creating and verifying
[JSON Web Tokens (JWTs)](https://tools.ietf.org/html/rfc7519) in Python. It allows you to once define the claims of the
JWT, and to then create and accept tokens with these claims without having to check if all the required data is given
or if the token actually is the one you expect.

Flask-EasyJWT is a simple wrapper around [EasyJWT](https://github.com/BMeu/EasyJWT) for easy usage in
[Flask](http://flask.pocoo.org/) applications. It provides configuration options via Flask's application configuration
for common settings of all tokens created in a web application. For detailed information on how to use
[EasyJWT](https://github.com/BMeu/EasyJWT), see [its documentation](https://easyjwt.readthedocs.org/en/latest/).

```python
from flask_easyjwt import FlaskEasyJWT
from flask import Flask

# Define the claims of your token.
class MySuperSimpleJWT(FlaskEasyJWT):

    def __init__(self, key):
        super().__init__(key)
        
        # Define a claim `name`.
        self.name = None

# Define the default configuration options for FlaskEasyJWT
# in the configuration of your Flask app.
app = Flask(__name__)
app.config.from_mapping(
    # The default key for encoding and decoding tokens.
    EASYJWT_KEY='Super secret key',

    # Tokens will be valid for 15 minutes after creation by default.
    EASYJWT_TOKEN_VALIDITY=15 * 60
)

@app.route('/token/<name>')
def get_token(name):
    """ This view returns a token with the given name as its value. """
    token_object = MySuperSimpleJWT()
    token_object.name = name
    return token_object.create()

@app.route('/verify/<token>')
def verify_token(token):
    """ This view verifies the given token and returns the contained name. """
    verified_token_object = MySuperSimpleJWT.verify(token)
    return verified_token_object.name
```

## Features

 * Integrates [EasyJWT](https://github.com/BMeu/EasyJWT) into Flask for easy configuration of default options for
   creating and verifying JWTs.
 * Define the claims of your token once as a class, then use this class to easily create and verify multiple tokens.
 * No worries about typos in dictionary keys: the definition of your claim set as a class enables IDEs to find those
   typos for you.
 * Multiple tokens may have the same claims, but different intentions. Flask-EasyJWT will take care of this for you: you
   can define a token for account validation and one for account deletion, both with the account ID as a claim, and you
   don't need to worry about accidentally deleting a newly created account instead of validating it, just because
   someone mixed up the tokens.
 * All registered JWT claims are supported: `aud`, `exp`, `iat`, `iss`, `jti`, `nbf`, and `sub`.

For a full list of features, see [the features of EasyJWT](https://easyjwt.readthedocs.org/en/latest/#features).

## System Requirements & Installation

Flask-EasyJWT requires Python 3.6 or newer.

Flask-EasyJWT is available [on PyPI](https://pypi.org/project/flask_easyjwt/). You can install it using your favorite
package manager.

 * PIP:

    ```bash
    python -m pip install flask_easyjwt
    ```

 * Pipenv:

    ```bash
    pipenv install flask_easyjwt
    ```

## Usage

## Acknowledgements

Flask-EasyJWT is just an easy-to-use abstraction layer around José Padilla's
[PyJWT library](https://pypi.org/project/PyJWT/) that does the actual work of creating and verifying the tokens
according to the JWT specification. Without his work, Flask-EasyJWT would not be possible.

## License

Flask-EasyJWT is developed by [Bastian Meyer](https://www.bastianmeyer.eu)
<[bastian@bastianmeyer.eu](mailto:bastian@bastianmeyer.eu)> and is licensed under the
[MIT License]((http://www.opensource.org/licenses/MIT)). For details, see the attached [LICENSE](LICENSE) file. 
