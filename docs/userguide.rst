
User Guide
==========
Unit tests in TAPI are specified via a json file. i.e. You specify the input and describe what the output should look
like. (Optionally specifying some confirmation steps as well)

The default name of the json file is tapi.json. However, you could name it something diferrent and run it like:

    python tapi.py -c <my_new_config>.json

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
      "startup": [...],
      "teardown": [...],
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
| startup          | list   | []       | No       | actions to perform before **each** test runs                      |
+------------------+--------+----------+----------+-------------------------------------------------------------------+
| teardown         | list   | []       | No       | actions to perform after **each** test runs                       |
+------------------+--------+----------+----------+-------------------------------------------------------------------+
| tests            | list   | []       | Yes      | tests to be run                                                   |
+------------------+--------+----------+----------+-------------------------------------------------------------------+

The following subsections will detail the individual compound keys. (ROOT indicates the root of the json structure.)

ROOT:common
+++++++++++

This element contains all the request params that will be common to all requests made by Tapi. It can also contain a response section that can contain all data that needs to be validated. Here is a sample:

.. code-block:: javascript

    {
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

The above snippet will send the accept-encoding header to 'compress, gzip' in every request made by Tapi (unless overidden in the test config itself). When a response arrives, it will check if the status code is 200 and the response header content-type is set to 'application/json'. Else a failure is recorded.

ROOT:on_failure
+++++++++++++++

This determines what should be done in case a test fails. Possible values are 'continue' and 'abort'


ROOT:startup_harness
++++++++++++++++++++

These are API calls that are made before the test run. It's essentialy a list of 'ROOT:common' sections. It's called only once during the entire run at the beginning. A sample harness is as follows:

.. code-block:: javascript

    [{
        "request": {
            "url": "http://api.example.com/init1"
        }
    },
    {
        "request": {
            "url": "http://api.example.com/init2"
        }
    },
    {
        "request": {
            "url": "http://api.example.com/init3"
        }
    }
    ]

Note that the response status code is verified by default. If any request fails, the tests do not begin.

ROOT:teardown_harness
+++++++++++++++++++++

These are API calls that are made after all tests run. It's essentialy a list of 'ROOT:common' sections. It's called only once during the entire run at the end. A sample harness is as follows:

.. code-block:: javascript

    [{
        "request": {
            "url": "http://api.example.com/cleanup1"
        }
    },
    {
        "request": {
            "url": "http://api.example.com/cleanup2"
        }
    },
    {
        "request": {
            "url": "http://api.example.com/cleanup3"
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
                "request": {
                    "url": "/startup",
                    "verb": "post"
                }
            }
        ],
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
        },
        "confirm": {
          "request": {
            "url": "/endpoint/[[self._.response.body.name]]"
          },
          "response": {
            "body": {
              "$.name": "bob",
              "$.age": "20"
            }
          }
        },
        "teardown": [
            {
                "request": {
                    "url": "/teardown",
                    "verb": "post"
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
| id       | string |   None   | No       | unique id to identify this test. later tests may use this id as a key into             |
|          |        |          |          | a dict whose value is the particular test details like request/response etc.           |
|          |        |          |          | e.g. if a test id is 'foobar', a later test may reference it's request parameters like |
|          |        |          |          | this: self.foobar.request.url or self.foobar.request.payload.key                       |
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
|          |        |          |          | payload - dict of header key/value pairs (Optional)                                    |
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


**Note**:

1. It is the responsibility of the author to ensure that ids across all tests are unique. Else the json file will be rejected.
2. When matching headers, if the value is '*', then it merely checks for the existence of the header key, and any value is ok. This is used in places where the value is probably generated by the server on the fly, e.g. auth tokens.
3. When matching headers, the value is interpreted as a python regular expression pattern to match with the response received.

Field Inheritance
-----------------
One main idea behind the json format is that each test 'inherits' all parameters from it's parent. e.g. we can specify
a 'base_url' field in the ROOT of the json structure and then override it within a test. Similarly, you can set a global 
'on_failure' policy of continue|abort and then override it within the body of the individual test.










