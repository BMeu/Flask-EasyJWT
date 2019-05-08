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
for common settings of all tokens created in a web application.

## Features

## System Requirements & Installation

## Usage

## Acknowledgements

Flask-EasyJWT is just an easy-to-use abstraction layer around José Padilla's
[PyJWT library](https://pypi.org/project/PyJWT/) that does the actual work of creating and verifying the tokens
according to the JWT specification. Without his work, Flask-EasyJWT would not be possible.

## License

Flask-EasyJWT is developed by [Bastian Meyer](https://www.bastianmeyer.eu)
<[bastian@bastianmeyer.eu](mailto:bastian@bastianmeyer.eu)> and is licensed under the
[MIT License]((http://www.opensource.org/licenses/MIT)). For details, see the attached [LICENSE](LICENSE) file. 
