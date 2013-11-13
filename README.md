### Nuri

A happy little uri parsing and handy dandy little helper.

**Look at a few of the pieces that the parser can pick up on**

    python nuri.py http://bob.example/test/path\?query\=test%20this\&archived\=True

    Nuri URI Parsing
    ----------------
    input: http://bob.example/test/path?query=test%20this&archived=True
    scheme: http
    authority: bob.example
    path: /test/path
    query: {'query': 'test this', 'archived': 'True'}
    string: http://bob.example/test/path?query=test%20this&archived=True

**Need a little help with query params?**

    myuri = Uri("http://example.com/path/page")
    myuri.query_params["id"] = 1239
    str(myuri) == "http://example.com/path/page?id=1239"