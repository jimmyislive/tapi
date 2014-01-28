
User Guide
==========
Unit tests in TAPI are specified via a json file. i.e. You specify the input and describe what the output should look
like. (Optionally specifying some confirmation steps as well)

The default name of the json file is tapi.json. However, you could name it something diferrent and run it like:

    python tapi.py -c <my_new_config>.json

By default the above will also verify that the provided json file has the correct format and all required key/values are present etc.
If you only wish to verify the json file and not run any tests:

    python tapi.py -c <my_new_config>.json -v

You can also specify which test you wish to run by providing their ids: (default is to run all tests)

    python tapi.py -c <my_new_config>.json -i id1,id2,id3

See python tapi.py --help for more details.

Fundamentals
-------------

The fundamental elements in a tapi.json file is the request/response elements. A request element looks like:

.. code-block:: javascript

    {
        "request": {
            "url": "<some url>",
            "verb": "get",
            "headers": {
                "header_key1": "header_value1",
                "header_key2": "header_value2",
            },
            "payload": {
                "payload_key1": "payload_value1",
                "payload_key2": "payload_value2",
            }
        }
    }

The only required field in the above is the 'url' field. The above snippet will cause a GET request to be made to the url
<some url> along with headers as in the field 'headers' and the 'payload' form encoded.

The 'verb' defaults to GET. Other possible values are POST/PUT/DELETE

A response element looks like:

.. code-block:: javascript

    {
        "response": {
            "status_code": 200,
            "headers": {
                "header_key1": "header_value1",
                "header_key2": "header_value2"
            },
            "body": {
                "$.name": "foobar"
            }
        }
    }

The response subsection is typically optional. Add it if you need to check something other than the defaults. The default status_code is 200. The block causes the framework to verify that the response received after making the HTTP request (as
defined by the 'request' section) matches the values specified. If it does not, a failure is reported.

Primary Elements
-----------------

There are 4 main primary subsections in a test:

1. startup
2. main
3. confirm
4. teardown

A startup section is a list of main/confirm subsections. These are run in order before any test. The idea is to do any 
setup like functionality in these blocks. It is always optional.

A main subsection details the api being tested. It is the only required subsection in any test.

A confirm subsection typically is an api call to confirm that the api being tested actually did the work. e.g. if you are 
testing any api to add a user, a confirm subsection could do a GET on that user to ensure that the user was actually added.
It is always optional.

A teardown is run at the end of each test. It is to perform any possible cleanup action you may have. it is always optional.

Overall Structure
-----------------

The tapi.json file has the following overall structure:

.. code-block:: javascript

    {
      "heading": "Some heading for what you are testing",
      "base_url": "http://api.example.com",
      "common": {...},
      "on_failure": "continue",
      "startup_harness": [...],
      "teardown_harness": [...],
      "tests": [...]
    }

The field descriptions are as follows:

+------------------+--------+----------+----------+-------------------------------------------------------------------+
| Field            | Type   | Default  | Required | Description                                                       |
+==================+========+==========+==========+===================================================================+
| heading          | string |   None   | No       | a human friendly name for this test suite                         |
+------------------+--------+----------+----------+-------------------------------------------------------------------+
| base_url         | string |   None   | No       | the base url to prepend to every url path specified in the tests  |
+------------------+--------+----------+----------+-------------------------------------------------------------------+
| common           | dict   |    {}    | No       | common parameters for requests/response                           |
+------------------+--------+----------+----------+-------------------------------------------------------------------+
| on_failure       | string | continue | No       | action in case of failure. (continue/abort)                       |
+------------------+--------+----------+----------+-------------------------------------------------------------------+
| startup_harness  | list   | []       | No       | actions to perform before the run begins                          |
+------------------+--------+----------+----------+-------------------------------------------------------------------+
| teardown_harness | list   | []       | No       | actions to perform after the test run                             |
+------------------+--------+----------+----------+-------------------------------------------------------------------+
| tests            | list   | []       | Yes      | tests to be run                                                   |
+------------------+--------+----------+----------+-------------------------------------------------------------------+

The following subsections will detail the individual compound keys. (ROOT indicates the root of the json structure.)

ROOT:common
+++++++++++

This element contains all the request params that will be common to all requests made by Tapi. It can also contain a response section that can contain all data that needs to be validated. Here is a sample:

.. code-block:: javascript

    {
        "main": {
            "request": {
                "headers": {
                    "accept-encoding": "compress, gzip"
                }
            }
            "response": {
                "status_code": 200,
                "headers": { 
                    "content-type": "application/json"
                }
            }
        }
    }

The above snippet will send the accept-encoding header to 'compress, gzip' in every request made by Tapi (unless overidden in the test config itself). When a response arrives, it will check if the status code is 200 and the response header content-type is set to 'application/json'. Else a failure is recorded.

ROOT:on_failure
+++++++++++++++

This determines what should be done in case a test fails. Possible values are 'continue' and 'abort'


ROOT:startup_harness
++++++++++++++++++++

These are API calls that are made before the test run. It's called only once during the entire run at the beginning. A sample harness is as follows:

.. code-block:: javascript

    [{
        "main": {
            "request": {
                "url": "http://api.example.com/init1"
            }
        }
    },
    {
        "main": {
            "request": {
                "url": "http://api.example.com/init2"
            }
        }
    },
    {
        "main": {
            "request": {
                "url": "http://api.example.com/init3"
            }
        }
    }
    ]

Note that the response status code is verified by default. If any request fails, the tests do not begin.

ROOT:teardown_harness
+++++++++++++++++++++

These are API calls that are made after all tests run. It's essentialy a list of 'ROOT:common' sections. It's called only once during the entire run at the end. A sample harness is as follows:

.. code-block:: javascript

    [{
        "main": {
            "request": {
                "url": "http://api.example.com/cleanup1"
            }
        }
    },
    {
        "main": {
            "request": {
                "url": "http://api.example.com/cleanup2"
            }
        }
    },
    {
        "main": {
            "request": {
                "url": "http://api.example.com/cleanup3"
            }
        }
    }
    ]

Note that the response status code is verified by default. If any request fails, the test run is indicated as a failure.

ROOT:tests
++++++++++

This is essentially the meat of the framework. It's where all the requests to test each endpoint is specified. It contains a list of sections wherein each section specifies how an endpoint should be requested and how the response should be verfied. Here is an example of a individual test:

.. code-block:: javascript

    {
        "name": "new user",
        "id": "new_user",
        "startup": [ 
            {
                "main": {
                    "request": {
                        "url": "/startup",
                        "verb": "post"
                    }
                }
            }
        ],
        "main": {
            "request": {
              "url": "/endpoint",
              "verb": "post",
              "payload": {
                "name": "bob",
                "age": "20"
              }
            },
            "response": {
                "status_code": 201,
                "headers": {
                    "auth-token": "*"
                }
                "body": {
                    "$.name": "bob"
                }
            }
        },
        "confirm": {
            "main": {
                "request": {
                    "url": "/endpoint/[[self._.response.body.name]]"
                  },
                  "response": {
                    "body": {
                      "$.name": "bob",
                      "$.age": "20"
                    }
                }
            }
        },
        "teardown": [
            {
                "main": {
                    "request": {
                        "url": "/teardown",
                        "verb": "post"
                    }
                }
            }
        ]
    }

The field descriptions are as follows:

+----------+--------+----------+----------+----------------------------------------------------------------------------------------+
| Field    | Type   | Default  | Required | Description                                                                            |
+==========+========+==========+==========+========================================================================================+
| name     | string |   None   | Yes      | a human friendly name for the test                                                     |
+----------+--------+----------+----------+----------+-----------------------------------------------------------------------------+
| id       | string |   None   | No       | unique id to identify this test.                                                       |
+----------+--------+----------+----------+----------------------------------------------------------------------------------------+
| startup  | list   | None     | No       | list of endpoints to call before running the test                                      |
+----------+--------+----------+----------+----------+-----------------------------------------------------------------------------+
| teardown | list   | None     | No       | list of endpoints to call after running the test                                       |
+----------+--------+----------+----------+----------+-----------------------------------------------------------------------------+
| request  | dict   | None     | Yes      | request object. Possible keys are:                                                     |
|          |        |          |          |                                                                                        |
|          |        |          |          | url - url to test (Required)                                                           |
|          |        |          |          |                                                                                        |
|          |        |          |          | verb - HTTP verb (defaults to GET) (Optional)                                          |
|          |        |          |          |                                                                                        |
|          |        |          |          | headers - dict of header key/value pairs (Optional)                                    |
|          |        |          |          |                                                                                        |
|          |        |          |          | payload - dict of key/value pairs or a string (Optional). If a dict is given, it will  |
|          |        |          |          | be url-encoded. If string, it will be used as is.                                      |
+----------+--------+----------+----------+----------+-----------------------------------------------------------------------------+
| response | dict   | None     | No       | response object to be verified. Possible keys are:                                     |
|          |        |          |          |                                                                                        |
|          |        |          |          | status_code - what should the response code be? (default 200) (Optional)               |
|          |        |          |          |                                                                                        |
|          |        |          |          | headers - dict of response header key/value pairs that need to match (Optional)        |
|          |        |          |          |                                                                                        |
|          |        |          |          | body - dict of key/value pairs that need to match (Optional) Use the                   |
|          |        |          |          |        `jsonpath-rw <https://github.com/kennknowles/python-jsonpath-rw>`_ spec         |
|          |        |          |          |        to match values in the body.                                                    |
+----------+--------+----------+----------+----------+-----------------------------------------------------------------------------+
| confirm  | dict   | None     | No       | confirm that the API request just worked. It consists of a request/response block.     |
|          |        |          |          | e.g. if the request block was adding a user, the response block would have verfied it, |
|          |        |          |          | the confirm block can be used to do a GET at the final user endpoint to confirm that   |
|          |        |          |          | user was indeed added.                                                                 |
+----------+--------+----------+----------+----------+-----------------------------------------------------------------------------+


Tapi Expressions
-----------------
In so happens sometimes that the values of fields need to be computed and are not readily available. e.g. we may want
to add an 'authorization' header with has the sha256 hash of the username:password or something similar. In order to facilitate
such situations, you can use Script Tapi Expressions. These are essentially python scripts that take some parameters and output a result.

There are three types of Script Tapi Expressions, one for requests, one for responses and one for tokens. The one for requests always returns a value which is used in the HTTP request. The script for response is one that takes some args and always returns True/False i.e. telling us if the response matched the spec or not.

A sample request tapi expression is like:

.. code-block:: javascript

    {
        "request": {
            "main": {
                "url": "http://www.api.example.com",
                "id": "some_id",
                "verb": "post",
                "headers": {
                    "authorization": "[[script:request_some_id_authorization.py]]"
                },
                "payload": "[[script:request_some_id_payload.py]]"
            }
        }
    }

The framework will then look for the script request_some_id_authorization.py/request_some_id_payload.py in the same directory as the tapi.json (or whatever you have named your config as) and execute it. The return value of the script is then used when making the HTTP request.

The request scripts should have this general form:

.. code-block:: python

    class RequestRunner(object):

        @classmethod
        def get_value(cls, test_output_so_far, config_data):

            #do whatever you need here...

            return 'some value'

The framework will import RequestRunner and calls method get_value. The argument test_output_so_far is a dict of the test 
request/response results of any previous subsections so far e.g. startup, main subsections etc. The config_data is the json
config of the test under consideration. Thus this function has all the info it needs and it can do whatever logic it wants to do
and finally return a result to be used as a value in the HTTP request.

Similarly the response tapi script has the form:

.. code-block:: python

    class ResponseRunner(object):

        @classmethod
        def validate(cls, test_output_so_far, test_config_data, response):

            return len(json.loads(response)) == 2

The framework will import ResponseRunner and call method validate. Args provided include the HTTP response object. The script 
can then do any calculation it neds and finally return a True/False answer.

Sometimes, we would also like to access the value of a previously calculated header in future subsections. e.g. the first time
you login, if you get a auth-token. And later in every subsequent API call, you need to specify that auth-token, you can use a token tapi expression:

.. code-block:: javascript

    {
        "main": {
            "request": {
                "url": "http://www.api.example.com/login",
                "id": "some_id",
                "verb": "post",
                "payload": {
                    "username": "foo",
                    "password": "bar",
                }
            },
            "response": {
                "headers": {
                    "auth-token": "*"
                }
            }
        },
        "confirm": {
            "request": {
                "url": "http://www.api.example.com/dashboard",
                "headers": {
                    "auth-token": "[[token:main.response.headers.auth-token]]"
                }
            }
        }
    }

The [[token:main.response.headers.auth-token]] tells the framework that the auth-token value should be the same as in the 
response header from the initial request. Note the asterix in the first api response. This tells the tapi framework to only
check for the existence of the key, any value returned by the server is ok.

Finally, you can also access environment vaiables by using a tapi expression like [[env:$USERNAME]] - this will be replaced
by the value of the $USERNAME environment variable.











