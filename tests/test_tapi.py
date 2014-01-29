#! /usr/bin/env python
#! -*- coding: utf-8 -*-

import json
import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tapi import Tapi, TapiExprEvaluator

__doc__ = """Unit tests for TAPI"""

class TapiConfigExampleTests(unittest.TestCase):

    """This tests all the examples specified in the documentation"""

    def test_simple1(self):
        tapi_json = '''{
            "heading": "simple1 example",
            "tests": [{
                "main": {
                    "request": {
                        "url": "http://api.example.com/users"
                    }
                }
            }]
        }'''
        tapi_obj = Tapi(json.loads(tapi_json))

        self.assertEqual(tapi_obj.heading, 'simple1 example')
        self.assertEqual(len(tapi_obj.tests), 1)
        self.assertEqual(tapi_obj.tests[0]['main']['request']['url'], 'http://api.example.com/users')

    def test_simple2(self):
        tapi_json = '''{
            "heading": "simple2 example",
            "tests": [{
                "main": {
                    "request": {
                        "url": "http://api.example.com/users",
                        "verb": "get"
                    },
                    "response": {
                        "status_code": 200
                    }
                }
            }]
        }'''
        tapi_obj = Tapi(json.loads(tapi_json))

        self.assertEqual(tapi_obj.heading, 'simple2 example')
        self.assertEqual(len(tapi_obj.tests), 1)
        self.assertEqual(tapi_obj.tests[0]['main']['request']['url'], 'http://api.example.com/users')
        self.assertEqual(tapi_obj.tests[0]['main']['request']['verb'], 'get')
        self.assertEqual(tapi_obj.tests[0]['main']['response']['status_code'], 200)

    def test_simple3(self):
        tapi_json = '''{
            "heading": "simple3 example",
            "tests": [{
                "main": {
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
                }
            }]
        }'''
        tapi_obj = Tapi(json.loads(tapi_json))

        self.assertEqual(tapi_obj.heading, 'simple3 example')
        self.assertEqual(len(tapi_obj.tests), 1)
        self.assertEqual(tapi_obj.tests[0]['main']['request']['url'], 'http://api.example.com/users')
        self.assertEqual(tapi_obj.tests[0]['main']['request']['verb'], 'post')
        self.assertEqual(tapi_obj.tests[0]['main']['request']['headers']['accept-encoding'], 'compress, gzip')
        self.assertEqual(tapi_obj.tests[0]['main']['request']['payload']['name'], 'bob')
        self.assertEqual(tapi_obj.tests[0]['main']['response']['status_code'], 201)

    def test_simple4(self):
        tapi_json = '''{
            "heading": "simple4 example",
            "tests": [{
                "main": {
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
                }
            }]
        }'''
        tapi_obj = Tapi(json.loads(tapi_json))

        self.assertEqual(tapi_obj.heading, 'simple4 example')
        self.assertEqual(len(tapi_obj.tests), 1)
        self.assertEqual(tapi_obj.tests[0]['main']['request']['url'], 'http://api.example.com/users/bob')
        self.assertEqual(tapi_obj.tests[0]['main']['request']['verb'], 'get')
        self.assertEqual(tapi_obj.tests[0]['main']['request']['headers']['accept-encoding'], 'compress, gzip')
        self.assertEqual(tapi_obj.tests[0]['main']['response']['status_code'], 200)
        self.assertEqual(tapi_obj.tests[0]['main']['response']['headers']['content-type'], 'application/json')
        self.assertEqual(tapi_obj.tests[0]['main']['response']['body']['$.name'], 'bob')

    def test_intermediate1(self):
        tapi_json = '''{
            "heading": "intermediate1 example",
            "base_url": "http://api.example.com",
            "common": {
                "main": {
                    "response": {
                      "status_code": 200,
                      "headers": { 
                        "content-type": "application/json"
                      }
                    }
                }
            },
            "on_failure": "abort",
            "tests": [{
                "main": {
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
        }'''
        tapi_obj = Tapi(json.loads(tapi_json))

        self.assertEqual(tapi_obj.heading, 'intermediate1 example')
        self.assertEqual(tapi_obj.base_url, 'http://api.example.com')
        self.assertEqual(tapi_obj.on_failure, 'abort')
        self.assertEqual(tapi_obj.common['main']['response']['status_code'], 200)
        self.assertEqual(tapi_obj.common['main']['response']['headers']['content-type'], 'application/json')
        self.assertEqual(len(tapi_obj.tests), 1)
        self.assertEqual(tapi_obj.tests[0]['main']['request']['url'], '/users/bob')
        self.assertEqual(tapi_obj.tests[0]['main']['request']['verb'], 'get')
        self.assertEqual(tapi_obj.tests[0]['main']['request']['headers']['accept-encoding'], 'compress, gzip')
        self.assertEqual(tapi_obj.tests[0]['main']['response']['body']['$.name'], 'bob')

    def test_intermediate2(self):
        tapi_json = '''{
            "heading": "intermediate2 example",
            "base_url": "http://api.example.com",
            "common": {
                "main": {
                    "response": {
                      "status_code": 200,
                      "headers": { 
                        "content-type": "application/json"
                      }
                    }
                }
            },
            "on_failure": "abort",
            "startup_harness": [{
                "main": {
                    "request": {
                        "url": "/init"
                    }
                }
            }],
            "teardown_harness": [{
                "main": {
                    "request": {
                        "url": "/cleanup"
                    }
                }
            }],
            "tests": [{
                "main": {
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
        }'''
        tapi_obj = Tapi(json.loads(tapi_json))

        self.assertEqual(tapi_obj.heading, 'intermediate2 example')
        self.assertEqual(tapi_obj.base_url, 'http://api.example.com')
        self.assertEqual(tapi_obj.on_failure, 'abort')
        self.assertEqual(tapi_obj.common['main']['response']['status_code'], 200)
        self.assertEqual(tapi_obj.common['main']['response']['headers']['content-type'], 'application/json')
        self.assertEqual(len(tapi_obj.tests), 1)
        self.assertEqual(len(tapi_obj.startup_harness), 1)
        self.assertEqual(len(tapi_obj.teardown_harness), 1)
        self.assertEqual(tapi_obj.tests[0]['main']['request']['url'], '/users/bob')
        self.assertEqual(tapi_obj.tests[0]['main']['request']['verb'], 'get')
        self.assertEqual(tapi_obj.tests[0]['main']['request']['headers']['accept-encoding'], 'compress, gzip')
        self.assertEqual(tapi_obj.tests[0]['main']['response']['body']['$.name'], 'bob')

    def test_advanced1(self):
        tapi_json = '''{
            "heading": "advanced1 example",
            "base_url": "http://api.example.com",
            "common": {
                "main": {
                    "response": {
                      "status_code": 200,
                      "headers": { 
                        "content-type": "application/json"
                      }
                    }
                }
            },
            "on_failure": "abort",
            "startup_harness": [{
                "main": {
                    "request": {
                        "url": "/init"
                    }
                }
                
            }],
            "teardown_harness": [{
                "main": {
                    "request": {
                        "url": "/cleanup"
                    }
                }
            }],
            "tests": [
                { 
                    "main": {
                        "request": {
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
                    },
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
        }'''
        tapi_obj = Tapi(json.loads(tapi_json))

        self.assertEqual(tapi_obj.heading, 'advanced1 example')
        self.assertEqual(tapi_obj.base_url, 'http://api.example.com')
        self.assertEqual(tapi_obj.on_failure, 'abort')
        self.assertEqual(tapi_obj.common['main']['response']['status_code'], 200)
        self.assertEqual(tapi_obj.common['main']['response']['headers']['content-type'], 'application/json')
        self.assertEqual(len(tapi_obj.tests), 1)
        self.assertEqual(len(tapi_obj.startup_harness), 1)
        self.assertEqual(len(tapi_obj.teardown_harness), 1)
        self.assertEqual(tapi_obj.tests[0]['main']['request']['url'], '/users')
        self.assertEqual(tapi_obj.tests[0]['main']['request']['verb'], 'post')
        self.assertEqual(tapi_obj.tests[0]['confirm']['request']['url'], '/users/bob')
        self.assertEqual(tapi_obj.tests[0]['confirm']['request']['headers']['accept-encoding'], 'compress, gzip')
        self.assertEqual(tapi_obj.tests[0]['confirm']['response']['body']['$.name'], 'bob')

    def test_advanced2(self):
        tapi_json = '''{
            "heading": "advanced2 example",
            "base_url": "http://api.example.com",
            "common": {
                "main": {
                    "response": {
                      "status_code": 200,
                      "headers": { 
                        "content-type": "application/json"
                      }
                    }
                }
            },
            "on_failure": "abort",
            "startup_harness": [{
                "main": {
                    "request": {
                        "url": "/init"
                    }
                }
            }],
            "teardown_harness": [{
                "main": {
                    "request": {
                        "url": "/cleanup"
                    }
                }
            }],
            "tests": [
                { 
                    "main": {
                        "request": {
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
                    },
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

                { 
                    "main": {
                        "request": {
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
                    },
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
        }'''
        tapi_obj = Tapi(json.loads(tapi_json))

        self.assertEqual(tapi_obj.heading, 'advanced2 example')
        self.assertEqual(tapi_obj.base_url, 'http://api.example.com')
        self.assertEqual(tapi_obj.on_failure, 'abort')
        self.assertEqual(tapi_obj.common['main']['response']['status_code'], 200)
        self.assertEqual(tapi_obj.common['main']['response']['headers']['content-type'], 'application/json')
        self.assertEqual(len(tapi_obj.tests), 2)
        self.assertEqual(len(tapi_obj.startup_harness), 1)
        self.assertEqual(len(tapi_obj.teardown_harness), 1)
        self.assertEqual(tapi_obj.tests[0]['main']['request']['url'], '/users')
        self.assertEqual(tapi_obj.tests[0]['main']['request']['verb'], 'post')
        self.assertEqual(tapi_obj.tests[0]['confirm']['request']['url'], '/users/bob')
        self.assertEqual(tapi_obj.tests[0]['confirm']['request']['headers']['accept-encoding'], 'compress, gzip')
        self.assertEqual(tapi_obj.tests[0]['confirm']['response']['body']['$.name'], 'bob')
        self.assertEqual(tapi_obj.tests[1]['main']['request']['url'], '/users')
        self.assertEqual(tapi_obj.tests[1]['main']['request']['verb'], 'post')
        self.assertEqual(tapi_obj.tests[1]['confirm']['response']['body']['$.name'], 'jane')

    def test_advanced3(self):
        tapi_json = '''{
            "heading": "advanced3 example",
            "base_url": "http://api.example.com",
            "common": {
                "main": {
                    "response": {
                      "status_code": 200,
                      "headers": { 
                        "content-type": "application/json"
                      }
                    }
                },
                "startup": [
                    {
                        "main": {
                            "request": {
                                "url": "/start_timer"
                            }
                        }
                    }
                ],
                "teardown": [
                    {
                        "main": {
                            "request": {
                                "url": "/end_timer"
                            }
                        }
                    }
                ]
            },
            "on_failure": "abort",
            "startup_harness": [{
                "main": {
                    "request": {
                        "url": "/init"
                    }
                }
            }],
            "teardown_harness": [{
                "main": {
                    "request": {
                        "url": "/cleanup"
                    }
                }
            }],
            "tests": [
                { 
                    "main": {
                        "request": {
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
                    },
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

                { 
                    "main": {
                        "request": {
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
                    },
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
        }'''
        tapi_obj = Tapi(json.loads(tapi_json))

        self.assertEqual(tapi_obj.heading, 'advanced3 example')
        self.assertEqual(tapi_obj.base_url, 'http://api.example.com')
        self.assertEqual(tapi_obj.on_failure, 'abort')
        self.assertEqual(tapi_obj.common['main']['response']['status_code'], 200)
        self.assertEqual(tapi_obj.common['main']['response']['headers']['content-type'], 'application/json')
        self.assertEqual(len(tapi_obj.tests), 2)
        self.assertEqual(len(tapi_obj.startup_harness), 1)
        self.assertEqual(len(tapi_obj.teardown_harness), 1)
        self.assertEqual(tapi_obj.startup_harness[0]['main']['request']['url'], '/init')
        self.assertEqual(tapi_obj.teardown_harness[0]['main']['request']['url'], '/cleanup')
        self.assertEqual(tapi_obj.common['startup'][0]['main']['request']['url'], '/start_timer')
        self.assertEqual(tapi_obj.common['teardown'][0]['main']['request']['url'], '/end_timer')
        self.assertEqual(tapi_obj.tests[0]['main']['request']['url'], '/users')
        self.assertEqual(tapi_obj.tests[0]['main']['request']['verb'], 'post')
        self.assertEqual(tapi_obj.tests[0]['confirm']['request']['url'], '/users/bob')
        self.assertEqual(tapi_obj.tests[0]['confirm']['request']['headers']['accept-encoding'], 'compress, gzip')
        self.assertEqual(tapi_obj.tests[0]['confirm']['response']['body']['$.name'], 'bob')
        self.assertEqual(tapi_obj.tests[1]['main']['request']['url'], '/users')
        self.assertEqual(tapi_obj.tests[1]['main']['request']['verb'], 'post')
        self.assertEqual(tapi_obj.tests[1]['confirm']['response']['body']['$.name'], 'jane')

    def test_advanced4(self):
        tapi_json = '''{
            "heading": "advanced4 example",
            "base_url": "http://api.example.com",
            "common": {
                "main": {
                    "response": {
                      "status_code": 200,
                      "headers": { 
                        "content-type": "application/json"
                      }
                    }
                },
                "startup": [
                    {
                        "main": {
                            "request": {
                                "url": "/start_timer"
                            }
                        }
                    }
                ],
                "teardown": [
                    {
                        "main": {
                            "request": {
                                "url": "/end_timer"
                            }
                        }
                    }
                ]
            },
            "on_failure": "abort",
            "startup_harness": [{
                "main": {
                    "request": {
                        "url": "/init"
                    }
                }
            }],
            "teardown_harness": [{
                "main": {
                    "request": {
                        "url": "/cleanup"
                    }
                }
            }],
            "tests": [
                { 
                    "main": {
                        "request": {
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
                    },
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

                { 
                    "main": {
                        "request": {
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
                    },
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
                            "main": {
                                "request": {
                                    "url": "/start_jane_timer"
                                }
                            }
                        }
                    ],
                    "teardown": [
                        {
                            "main": {
                                "request": {
                                    "url": "/stop_jane_timer"
                                }
                            }
                        }
                    ]
                }
                ]
        }'''
        tapi_obj = Tapi(json.loads(tapi_json))

        self.assertEqual(tapi_obj.heading, 'advanced4 example')
        self.assertEqual(tapi_obj.base_url, 'http://api.example.com')
        self.assertEqual(tapi_obj.on_failure, 'abort')
        self.assertEqual(tapi_obj.common['main']['response']['status_code'], 200)
        self.assertEqual(tapi_obj.common['main']['response']['headers']['content-type'], 'application/json')
        self.assertEqual(len(tapi_obj.tests), 2)
        self.assertEqual(len(tapi_obj.startup_harness), 1)
        self.assertEqual(len(tapi_obj.teardown_harness), 1)
        self.assertEqual(tapi_obj.startup_harness[0]['main']['request']['url'], '/init')
        self.assertEqual(tapi_obj.teardown_harness[0]['main']['request']['url'], '/cleanup')
        self.assertEqual(tapi_obj.common['startup'][0]['main']['request']['url'], '/start_timer')
        self.assertEqual(tapi_obj.common['teardown'][0]['main']['request']['url'], '/end_timer')
        self.assertEqual(tapi_obj.tests[0]['main']['request']['url'], '/users')
        self.assertEqual(tapi_obj.tests[0]['main']['request']['verb'], 'post')
        self.assertEqual(tapi_obj.tests[0]['confirm']['request']['url'], '/users/bob')
        self.assertEqual(tapi_obj.tests[0]['confirm']['request']['headers']['accept-encoding'], 'compress, gzip')
        self.assertEqual(tapi_obj.tests[0]['confirm']['response']['body']['$.name'], 'bob')
        self.assertEqual(tapi_obj.tests[1]['main']['request']['url'], '/users')
        self.assertEqual(tapi_obj.tests[1]['main']['request']['verb'], 'post')
        self.assertEqual(tapi_obj.tests[1]['confirm']['response']['body']['$.name'], 'jane')
        self.assertEqual(tapi_obj.tests[1]['startup'][0]['main']['request']['url'], '/start_jane_timer')
        self.assertEqual(tapi_obj.tests[1]['teardown'][0]['main']['request']['url'], '/stop_jane_timer')

    def test_advanced5(self):
        tapi_json = '''{
            "heading": "advanced5 example",
            "base_url": "http://api.example.com",
            "common": {
                "main": {
                    "response": {
                      "status_code": 200,
                      "headers": { 
                        "content-type": "application/json"
                      }
                    }
                },
                "startup": [
                    {
                        "main": {
                            "request": {
                                "url": "/start_timer"
                            }
                        }
                    }
                ],
                "teardown": [
                    {
                        "main": {
                            "request": {
                                "url": "/end_timer"
                            }
                        }
                    }
                ]
            },
            "on_failure": "abort",
            "startup_harness": [{
                "main": {
                    "request": {
                        "url": "/init"
                    }
                }
            }],
            "teardown_harness": [{
                "main": {
                    "request": {
                        "url": "/cleanup"
                    }
                }
            }],
            "tests": [ 
                {   
                    "id": "postuser",
                    "startup": [
                        {
                            "main": {
                                "request": {
                                    "url": "/login",
                                    "verb": "post",
                                    "payload": {
                                        "name": "[[env:$USERNAME]]",
                                        "password": "[[env:$PASSWORD]]"
                                    }
                                },
                                "response": {
                                    "status_code": 200,
                                    "headers": {
                                        "auth-token": "*"
                                    }
                                }
                            }
                        }
                    ],
                    "main": {
                        "request": {
                            "url": "/users",
                            "verb": "post",
                            "payload": {
                                "name": "bob",
                                "age": 20,
                                "bank": "[[script:request_postuser_bank.py]]"
                            },
                            "headers": {
                                "auth-token": "[[token:startup[0].main.response.headers.auth-token]]"
                            }
                        },
                        "response": {
                            "status_code": 201,
                            "body": "[[script:response_postuser_body.py]]"
                        }
                    },
                    "confirm": {
                        "request": {
                            "url": "/users/bob",
                            "verb": "get",
                            "headers": {
                                "accept-encoding": "compress, gzip",
                                "auth-token": "[[token:startup[0].main.response.headers.auth-token]]"
                            }
                        },
                        "response": {
                            "body": {
                                "$.name": "bob"
                            }
                        }
                    }
                }
                ]
        }'''
        tapi_obj = Tapi(json.loads(tapi_json))

        self.assertEqual(tapi_obj.heading, 'advanced5 example')
        self.assertEqual(tapi_obj.base_url, 'http://api.example.com')
        self.assertEqual(tapi_obj.on_failure, 'abort')
        self.assertEqual(tapi_obj.common['main']['response']['status_code'], 200)
        self.assertEqual(tapi_obj.common['main']['response']['headers']['content-type'], 'application/json')
        self.assertEqual(len(tapi_obj.tests), 1)
        self.assertEqual(len(tapi_obj.startup_harness), 1)
        self.assertEqual(len(tapi_obj.teardown_harness), 1)
        self.assertEqual(tapi_obj.startup_harness[0]['main']['request']['url'], '/init')
        self.assertEqual(tapi_obj.teardown_harness[0]['main']['request']['url'], '/cleanup')
        self.assertEqual(tapi_obj.common['startup'][0]['main']['request']['url'], '/start_timer')
        self.assertEqual(tapi_obj.common['teardown'][0]['main']['request']['url'], '/end_timer')
        self.assertEqual(tapi_obj.tests[0]['main']['request']['url'], '/users')
        self.assertEqual(tapi_obj.tests[0]['main']['request']['verb'], 'post')
        self.assertEqual(tapi_obj.tests[0]['confirm']['request']['url'], '/users/bob')
        self.assertEqual(tapi_obj.tests[0]['confirm']['request']['headers']['accept-encoding'], 'compress, gzip')
        self.assertEqual(tapi_obj.tests[0]['confirm']['response']['body']['$.name'], 'bob')
        self.assertEqual(tapi_obj.tests[0]['startup'][0]['main']['request']['payload']['name'], '[[env:$USERNAME]]')
        self.assertEqual(tapi_obj.tests[0]['startup'][0]['main']['request']['payload']['password'], '[[env:$PASSWORD]]')
        self.assertEqual(tapi_obj.tests[0]['main']['request']['payload']['bank'], '[[script:request_postuser_bank.py]]')
        self.assertEqual(tapi_obj.tests[0]['main']['request']['headers']['auth-token'], '[[token:startup[0].main.response.headers.auth-token]]')
        self.assertEqual(tapi_obj.tests[0]['main']['response']['body'], '[[script:response_postuser_body.py]]')

class TapiExprTests(unittest.TestCase):

    """Tests for the different kinds of tapi expressions"""

    def test_is_tapi_expr(self):
        self.assertEqual(TapiExprEvaluator.is_tapi_expr('[[]]'), True)
        self.assertEqual(TapiExprEvaluator.is_tapi_expr('[]'), False)
        self.assertEqual(TapiExprEvaluator.is_tapi_expr('[['), False)
        self.assertEqual(TapiExprEvaluator.is_tapi_expr(']]'), False)

    def test_tapi_request_script(self):
        value = '[[script:request_test_id_headers_authorization.py]]'
        self.assertEqual(TapiExprEvaluator.normalize_request_tapi_expr(value, {}, {}), 'hello auth header')

    def test_tapi_response_script(self):
        value = '[[script:response_test_id_body.py]]'
        self.assertEqual(TapiExprEvaluator.get_response_tapi_expr(value, {}, {}, None), True)

    def test_tapi_token(self):
        test_output_so_far = {
            'main': {
                'response': {
                    'headers': {
                        'auth-token': '*'
                    }
                }
            }
        }
        value = '[[token:main.response.headers.auth-token]]'
        self.assertEqual(TapiExprEvaluator.normalize_request_tapi_expr(value, test_output_so_far, {}), '*')

    def test_tapi_env_var(self):
        os.environ['FOOBAR'] = 'foobar'
        value = '[[env:$FOOBAR]]'
        self.assertEqual(TapiExprEvaluator.normalize_request_tapi_expr(value, {}, {}), 'foobar')

if __name__ == '__main__':
    unittest.main()


