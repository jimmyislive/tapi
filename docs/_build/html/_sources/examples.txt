Examples
========

.. _Simple1_:

Simple1
-------

.. code-block:: javascript

    {
        "heading": "simple1 example",
        "tests": [{
            "request": {
                "url": "http://api.example.com/users"
            }
        }]
    }

The above makes a GET(default verb) request to the url and the response is verified to have a status code of 200 (default)

Simple2
-------

.. code-block:: javascript

    {
        "heading": "simple2 example",
        "tests": [{
            "request": {
                "url": "http://api.example.com/users",
                "verb": "get"
            },
            "response": {
                "status_code": 200
            }
        }]
    }

The same as Simple1_, it just makes the verb and status code checks explicit.

Simple3
-------

.. code-block:: javascript

    {
        "heading": "simple3 example",
        "tests": [{
            "request": {
                "url": "http://api.example.com/users",
                "verb": "post",
                "headers": {
                    "accept-encoding": "compress, gzip"
                },
                "payload": {
                    "name": "bob"
                }
            },
            "response": {
                "status_code": 201
            }
        }]
    }

This makes a POST request to the endpoint (api.example.com/users) with POST payload name=bob. It also adds a request header of Accept-Encoding as 'compress, gzip'. Response status_code is verified to be 201.

.. _Simple4:

Simple4
-------

.. code-block:: javascript

    {
        "heading": "simple4 example",
        "tests": [{
            "request": {
                "url": "http://api.example.com/users/bob",
                "verb": "get",
                "headers": {
                    "accept-encoding": "compress, gzip"
                }
            },
            "response": {
                "status_code": 200,
                "headers": {
                    "content-type": "application/json"
                },
                "body": {
                    "$.name": "bob"
                }
            }
        }]
    }

GETs user bob details and ensures that the response header of Content-Type is set to application/json and response body is a dict which has key/value pair name/bob.

.. _Intermediate1:

Intermediate1
-------------

.. code-block:: javascript

    {
        "heading": "simple4 example",
        "base_url": "http://api.example.com",
        "common": {
            "response": {
              "status_code": 200,
              "headers": { 
                "content-type": "application/json"
              }
            }
        },
        "on_failure": "abort",
        "tests": [{
            "request": {
                "url": "/users/bob",
                "verb": "get",
                "headers": {
                    "accept-encoding": "compress, gzip"
                }
            },
            "response": {
                "body": {
                    "$.name": "bob"
                }
            }
        }]
    }

Similar to Simple4_. It adds a base_url to the global 'common' section which will prepend base_url to every url parameter. Further it also says that every response should have a 200 status code and the Content-Type header should be set to application/json. Thus they have been removed from the tests[0]/response section as it is now redundant. It also specifies the action of 'abort' in case any test fails.

Intermediate2
-------------

.. code-block:: javascript

    {
        "heading": "simple4 example",
        "base_url": "http://api.example.com",
        "common": {
            "response": {
              "status_code": 200,
              "headers": { 
                "content-type": "application/json"
              }
            }
        },
        "on_failure": "abort",
        "startup_harness": [{
            "request": {
                "url": "/init",
            }
        }],
        "teardown_harness": [{
            "request": {
                "url": "/cleanup"
            }
        }],
        "tests": [{
            "request": {
                "url": "/users/bob",
                "verb": "get",
                "headers": {
                    "accept-encoding": "compress, gzip"
                }
            },
            "response": {
                "body": {
                    "$.name": "bob"
                }
            }
        }]
    }

Same as Intermediate1_, but it also specifies a startup/teardown action at the very begining and very end of the test run.

.. _Advanced1:

Advanced1
---------

.. code-block:: javascript

    {
        "heading": "simple4 example",
        "base_url": "http://api.example.com",
        "common": {
            "response": {
              "status_code": 200,
              "headers": { 
                "content-type": "application/json"
              }
            }
        },
        "on_failure": "abort",
        "startup_harness": [{
            "request": {
                "url": "/init",
            }
        }],
        "teardown_harness": [{
            "request": {
                "url": "/cleanup"
            }
        }],
        "tests": [
            { "request": {
                    "url": "/users",
                    "verb": "post",
                    "payload": {
                        "name": "bob",
                        "age": 20
                    }
                },
                "response": {
                    "status_code": 201
                }
                "confirm": {
                    "request": {
                        "url": "/users/bob",
                        "verb": "get",
                        "headers": {
                            "accept-encoding": "compress, gzip"
                        }
                    },
                    "response": {
                        "body": {
                            "$.name": "bob"
                        }
                    }
                }
            }]
    }

This example runs a test that has all three critical parts: request, response, confirmation. It posts data to the /users endpoint, verifies that the response is OK and then confirms that the API did indeed do what it said it was going to do by GETing the newly created resource.

.. _Advanced2:

Advanced2
---------

.. code-block:: javascript

    {
        "heading": "simple4 example",
        "base_url": "http://api.example.com",
        "common": {
            "response": {
              "status_code": 200,
              "headers": { 
                "content-type": "application/json"
              }
            }
        },
        "on_failure": "abort",
        "startup_harness": [{
            "request": {
                "url": "/init",
            }
        }],
        "teardown_harness": [{
            "request": {
                "url": "/cleanup"
            }
        }],
        "tests": [
            { "request": {
                    "url": "/users",
                    "verb": "post",
                    "payload": {
                        "name": "bob",
                        "age": 20
                    }
                },
                "response": {
                    "status_code": 201
                }
                "confirm": {
                    "request": {
                        "url": "/users/bob",
                        "verb": "get",
                        "headers": {
                            "accept-encoding": "compress, gzip"
                        }
                    },
                    "response": {
                        "body": {
                            "$.name": "bob"
                        }
                    }
                }
            },

            { "request": {
                    "url": "/users",
                    "verb": "post",
                    "payload": {
                        "name": "jane",
                        "age": 30
                    }
                },
                "response": {
                    "status_code": 201
                }
                "confirm": {
                    "request": {
                        "url": "/users/jane",
                        "verb": "get",
                        "headers": {
                            "accept-encoding": "compress, gzip"
                        }
                    },
                    "response": {
                        "body": {
                            "$.name": "jane"
                        }
                    }
                }
            }
            ]
    }

Similar to Advanced1_ but shows that you can add as many tests as you like because 'tests' is a list. In the above example we add a new user jane and verify that she has been added too.


Advanced3
---------

.. code-block:: javascript

    {
        "heading": "simple4 example",
        "base_url": "http://api.example.com",
        "common": {
            "response": {
              "status_code": 200,
              "headers": { 
                "content-type": "application/json"
              }
            }
        },
        "on_failure": "abort",
        "startup_harness": [{
            "request": {
                "url": "/init",
            }
        }],
        "teardown_harness": [{
            "request": {
                "url": "/cleanup"
            }
        }],
        "startup": [
            {
                "request": {
                    "url": "/start_timer"
                }
            }
        ]
        "teardown": [
            {
                "request": {
                    "url": "/end_timer"
                }
            }
        ],
        "tests": [
            { "request": {
                    "url": "/users",
                    "verb": "post",
                    "payload": {
                        "name": "bob",
                        "age": 20
                    }
                },
                "response": {
                    "status_code": 201
                }
                "confirm": {
                    "request": {
                        "url": "/users/bob",
                        "verb": "get",
                        "headers": {
                            "accept-encoding": "compress, gzip"
                        }
                    },
                    "response": {
                        "body": {
                            "$.name": "bob"
                        }
                    }
                }
            },

            { "request": {
                    "url": "/users",
                    "verb": "post",
                    "payload": {
                        "name": "jane",
                        "age": 30
                    }
                },
                "response": {
                    "status_code": 201
                }
                "confirm": {
                    "request": {
                        "url": "/users/jane",
                        "verb": "get",
                        "headers": {
                            "accept-encoding": "compress, gzip"
                        }
                    },
                    "response": {
                        "body": {
                            "$.name": "jane"
                        }
                    }
                }
            }
            ]
    }

Similar to Advanced2_, but here we also specify a global startup/teardown section. This will get called before **each** test run. (Note that the startup_harness/teardown_harness are called only once in their lifetime)

Advanced4
----------

.. code-block:: javascript

    {
        "heading": "simple4 example",
        "base_url": "http://api.example.com",
        "common": {
            "response": {
              "status_code": 200,
              "headers": { 
                "content-type": "application/json"
              }
            }
        },
        "on_failure": "abort",
        "startup_harness": [{
            "request": {
                "url": "/init",
            }
        }],
        "teardown_harness": [{
            "request": {
                "url": "/cleanup"
            }
        }],
        "startup": [
            {
                "request": {
                    "url": "/start_timer"
                }
            }
        ]
        "teardown": [
            {
                "request": {
                    "url": "/end_timer"
                }
            }
        ],
        "tests": [
            { "request": {
                    "url": "/users",
                    "verb": "post",
                    "payload": {
                        "name": "bob",
                        "age": 20
                    }
                },
                "response": {
                    "status_code": 201
                }
                "confirm": {
                    "request": {
                        "url": "/users/bob",
                        "verb": "get",
                        "headers": {
                            "accept-encoding": "compress, gzip"
                        }
                    },
                    "response": {
                        "body": {
                            "$.name": "bob"
                        }
                    }
                }
            },

            { "request": {
                    "url": "/users",
                    "verb": "post",
                    "payload": {
                        "name": "jane",
                        "age": 30
                    }
                },
                "response": {
                    "status_code": 201
                }
                "confirm": {
                    "request": {
                        "url": "/users/jane",
                        "verb": "get",
                        "headers": {
                            "accept-encoding": "compress, gzip"
                        }
                    },
                    "response": {
                        "body": {
                            "$.name": "jane"
                        }
                    }
                },
                "startup": [
                    {
                        "request": {
                            "url": "/start_jane_timer"
                        }
                    }
                ],
                "teardown": [
                    {
                        "request": {
                            "url": "/stop_jane_timer"
                        }
                    }
                ]
            }
            ]
    }

Similar to Advanced3_, but now user jane has her own custom startup/teardown section. This shows that the global parameters can be overridden within the test very easily.

Advanced5
---------

.. code-block:: javascript

    {
        "heading": "simple4 example",
        "base_url": "http://api.example.com",
        "common": {
            "response": {
              "status_code": 200,
              "headers": { 
                "content-type": "application/json"
              }
            }
        },
        "on_failure": "abort",
        "startup_harness": [{
            "request": {
                "url": "/init"
            }
        }],
        "teardown_harness": [{
            "request": {
                "url": "/cleanup"
            }
        }],
        "startup": [
            {
                "request": {
                    "url": "/start_timer"
                }
            }
        ],
        "teardown": [
            {
                "request": {
                    "url": "/end_timer"
                }
            }
        ],
        "tests": [ {
                "id": "login",
                "request": {
                    "url": "/login",
                    "verb": "post",
                    "payload": {
                        "name": "[[$USERNAME]]",
                        "password": "[[$PASSWORD]]"
                    }
                },
                "response": {
                    "status_code": 200,
                    "headers": {
                        "auth-token": "*"
                    }
                }
            },
            {   "id": "postuser",
                "request": {
                    "url": "/users",
                    "verb": "post",
                    "payload": {
                        "name": "bob",
                        "age": 20,
                        "bank": "[[script:request_postuser_bank]]"
                    },
                    "headers": {
                        "auth-token": "[[self.login.response.headers.auth-token]]"
                    }
                },
                "response": {
                    "status_code": 201,
                    "body": "[[script:response_postuser_body]]"
                },
                "confirm": {
                    "request": {
                        "url": "/users/bob",
                        "verb": "get",
                        "headers": {
                            "accept-encoding": "compress, gzip",
                            "auth-token": "[[self.login.response.headers.auth-token]]"
                        }
                    },
                    "response": {
                        "body": {
                            "$.name": "bob"
                        }
                    }
                }
            },

            { "request": {
                    "url": "/users",
                    "verb": "post",
                    "payload": {
                        "name": "jane",
                        "age": 30
                    },
                    "headers": {
                        "auth-token": "[[self.login.response.headers.auth-token]]"
                    }
                },
                "response": {
                    "status_code": 201
                },
                "confirm": {
                    "request": {
                        "url": "/users/jane",
                        "verb": "get",
                        "headers": {
                            "accept-encoding": "compress, gzip",
                            "auth-token": "[[self.login.response.headers.auth-token]]"
                        }
                    },
                    "response": {
                        "body": {
                            "$.name": "jane"
                        }
                    }
                },
                "startup": [
                    {
                        "request": {
                            "url": "/start_jane_timer"
                        }
                    }
                ],
                "teardown": [
                    {
                        "request": {
                            "url": "/stop_jane_timer"
                        }
                    }
                ]
            }
            ]
    }

Similar to Advanced4_, but here we begin everything with a test to /login. Note that we also assigned that test an id. We ensured that the response header has 'auth-token' (but don't worry about it's content, hence the star). In later tests, we want to send in the same auth-token in every request and we do this by aceesing the original auth-token via the id of the login test i.e. self.login.response.headers.auth-token. (remember to enclose it in [[]]). Also notice the [[$USERNAME]]. This means that the value of the environment variable $USERNAME is used here. The final point to notice is the ability to run arbitrary python scripts to either get some input value or verify some response result e.g. "bank": "[[script:request_postuser_bank]]". This means that the bank input parameter will be populated with the output of the script request_postuser_bank.py. Similarly "body": "[[script:response_postuser_body]]" means that the script response_postuser_body.py will be called and it's output should be True/False to indicate if it passed the check. Both scripts will receive the current unit test parametes as a json input. The convention is to name the python script as [request|response]_<id>_<field>.py. This way it will be easy to identify which test/field this script pertains to.




