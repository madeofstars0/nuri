### Nuri

A happy little uri parsing and handy dandy little helper.

**Need a little help with query params?**

    myuri = Uri("http://example.com/path/page")
    myuri.query_params["id"] = 1239
    str(myuri) == "http://example.com/path/page?id=1239"