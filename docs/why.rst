
Why use TAPI?
=============

Once you have built up your API server, comes the important task of testing it. (or is it the other way around :))
Testing APIs is a relatively simple, albeit time consuming task. It typically involves:

1. Make a request to an endpoint (using one of the verbs like GET, POST, PUT etc)
2. Verify the return status code/body etc

Most folks use their favourite testing tools (e.g. python unittest) and whip up tests cases that do just this. 
However, for something so simple, can one get away without writing any code?

That's what Tapi tries to do. You specify the APIs you want to test in a json file and also what the return codes should 
be. The Tapi framework takes care of making the request and checking the return code is as expected. You can also perform
other verifications like headers, content of body, executing yet another API call to ensure that some content has been
correctly POSTed etc.

Thus, Tapi makes testing your APIs as easy as editing a json file.
