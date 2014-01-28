Quick Start
===========

In order to start using Tapi you have to write a tapi.json file. The simplest tapi.json file looks like:

.. code-block:: javascript

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

The above means the following:

1. There is one test in this file
2. The framework will make a GET (the default) request to the endpoint api.example.com/users
3. The framework will verify that the return status code is 200 (default)

You can run this test by doing:
    python tapi.py

Thus, without writing a single line of code, you have successfully verfied that this endpoint works.
