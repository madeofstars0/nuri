import unittest
from uri import Uri

class GeneralTest(unittest.TestCase):
    def testClassInstatiates(self):
        myuri = Uri()
        self.assertIsNotNone(myuri)

class EasyHttpsUriParseTest(unittest.TestCase):
    def setUp(self):
        self.myuri = Uri("https://www.example.com/subdir/file.html")

    def testUriScheme(self):
        self.assertEqual("https", self.myuri.scheme)

    def testUriHost(self):
        self.assertEqual("www.example.com", self.myuri.host)

    def testUriPath(self):
        self.assertEqual("/subdir/file.html", self.myuri.path)

    def testUriQueryParams(self):
        self.assertEqual({}, self.myuri.query_params)


class EasyHttpUriParseTest(unittest.TestCase):
    def setUp(self):
        self.myuri = Uri("http://sub.example.com/directory/path")

    def testUriScheme(self):
        self.assertEqual("http", self.myuri.scheme)

    def testUriHost(self):
        self.assertEqual("sub.example.com", self.myuri.host)

    def testUriPath(self):
        self.assertEqual("/directory/path", self.myuri.path)

    def testUriQueryParams(self):
        self.assertEqual({}, self.myuri.query_params)

class EasyFileUriParseTest(unittest.TestCase):
    def setUp(self):
        self.myuri = Uri("file:///etc/nginx/sites-available/default")

    def testUriScheme(self):
        self.assertEqual("file", self.myuri.scheme)

    def testUriHost(self):
        self.assertEqual("", self.myuri.host)

    def testUriPath(self):
        self.assertEqual("/etc/nginx/sites-available/default", self.myuri.path)

    def testUriQueryParams(self):
        self.assertEqual({}, self.myuri.query_params)

class UriQueryParameterTest(unittest.TestCase):
    def testSingleQueryParam(self):
        myuri = Uri("bobo:/etc/files/a.conf?line=19")
        self.assertIn("line", myuri.query_params)
        self.assertEqual("19", myuri.query_params["line"])

class UriPathSegmentTest(unittest.TestCase):
    def testHttpDomainOnly(self):
        url = "http://example.com"
        myuri = Uri(url)
        self.assertIsNone(myuri.path_segments)
        self.assertEqual(str(myuri), url)

    def testHttpDomainOnlyWithQuery(self):
        url = "http://example.com?query=bob"
        myuri = Uri(url)
        self.assertIsNone(myuri.path_segments)
        self.assertEqual(str(myuri), url)

    def testHttpDomainRootPath(self):
        url = "http://example.com/"
        myuri = Uri(url)
        self.assertEqual(myuri.path_segments, [])
        self.assertEqual(str(myuri), url)

    def testHttpPath(self):
        url = "http://example.com/first/second/fifth/third/fourth?query=true"
        myuri = Uri(url)
        self.assertEqual(myuri.path_segments, ['first','second','fifth','third','fourth'])
        self.assertEqual(str(myuri), url)

    def testUrnPath(self):
        urn = "urn:usbn-13:1234567890123"
        myuri = Uri(urn)
        self.assertEqual(myuri.path_segments, ['usbn-13:1234567890123'])
        self.assertEqual(str(myuri), urn)

    def testHttpPathModification(self):
        myuri = Uri("http://example.com")
        myuri.path_segments = [] # there is no path in this url, so we need to init the array :(
        myuri.path_segments.append("test.html")
        self.assertEqual(str(myuri), "http://example.com/test.html")
        myuri.path_segments.insert(0, "directory")
        self.assertEqual(str(myuri), "http://example.com/directory/test.html")
        myuri.scheme = 'https'
        self.assertEqual(str(myuri), "https://example.com/directory/test.html")

class TrixyUriParseTest(unittest.TestCase):
    def testEmptyUri(self):
        myuri = Uri("")
        self.assertIsNotNone(myuri)
        self.assertIsNone(myuri.scheme)
        self.assertIsNone(myuri.authority)
        self.assertIsNone(myuri.host)
        self.assertIsNone(myuri.path)
        self.assertEqual({}, myuri.query_params)

    def testJustPathUri(self):
        myuri = Uri("path.html")
        self.assertIsNone(myuri.scheme)
        self.assertIsNone(myuri.authority)
        self.assertIsNone(myuri.host)
        self.assertEqual("path.html", myuri.path)
        self.assertEqual({}, myuri.query_params)  

    def testUrnUri(self):
        myuri = Uri("urn:path:to:nowhere")
        self.assertEqual(myuri.scheme, "urn")
        self.assertIsNone(myuri.authority)
        self.assertIsNone(myuri.host)
        self.assertEqual(myuri.path, "path:to:nowhere")
        self.assertEqual(myuri.query_params, {})    

    def testPathParsing(self):
        self.assertEqual(Uri("http://bob/abc?q=1").path, "/abc")
        self.assertEqual(Uri("http://bob/zyx#thing").path, "/zyx") 
        self.assertEqual(Uri("urn:/etc/path?abc#thing").path, "/etc/path")  

    def testIpHostParsing(self):
        self.assertEqual(Uri("http://10.0.0.1/bob.html").host, "10.0.0.1")
        self.assertEqual(Uri("http://[::1]/bob.html").host, "[::1]") 

class UriStringTest(unittest.TestCase):
    def testHttpToString(self):
        myuri = Uri("http://example.com/path/to/file.html")
        self.assertEqual(str(myuri), "http://example.com/path/to/file.html") 

    def testHttpWithParamsToString(self):
        myuri = Uri("http://example.com/path/to/file.html")
        myuri.query_params["test"] = "bob"
        self.assertEqual(str(myuri), "http://example.com/path/to/file.html?test=bob")
        myuri.query_params["id"] = 1234
        self.assertEqual(str(myuri), "http://example.com/path/to/file.html?test=bob&id=1234")

# Run the unit tests if called directly
if __name__ == '__main__':
    unittest.main()