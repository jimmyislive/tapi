
# TAPI - Testing APIs

Tapi is a framework for testing APIs

## Features

1. Test you API without writing any code (only edit a json file)
2. Test you APIs in a much more 'natural' way by specifying urls/verbs and what the output should be
3. Verify anything from response status codes, headers, body content etc
4. Also allows verification by issuing another API call to a different endpoint to ensure a prior API call worked
5. Execute arbitrary python scripts to populate request paramaters e.g. custom headers
6. Execute arbitrary python scripts to verify response from endpoint is valid
7. Tests your APIs using your own APIs

## Documentation

Documentation is available at http://tapi.readthedocs.org/en/latest/#

## Installation

pip install tapi

## Quickstart

In order to start using Tapi you have to write a tapi.json file. The simplest tapi.json file looks like:

```
    {
        "tests": [
            {
                "main": {
                    "request": {
                        "url": "http://api.example.com/users"
                    }
                }
            }
        ]
    }
```

The above means the following:

1. There is one test in this file named 'get all existing users'
2. The framework will make a GET (the default) request to the endpoint api.example.com/users
3. The framework will verify that the return status code is 200 (default)

You can run this test by doing:
    python tapi.py

Thus, without writing a single line of code, you have successfully verfied that this endpoint works.

No implementation as yet, details here: http://tapi.readthedocs.org/en/latest/#
