from nuri.uri import Uri
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Usage: %s url' % sys.argv[0])

    myuri = Uri(sys.argv[1])
    print 'Nuri URI Parsing'
    print '----------------'
    print "input: %s" % sys.argv[1]
    print "scheme: %s" % myuri.scheme
    print "authority: %s" % myuri.authority
    print "path: %s" % myuri.path
    print "query: %s" % str(myuri.query_params)
    print "string: %s" % str(myuri)
    print ""