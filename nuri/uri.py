
class Uri:
    """
    A class for dealing with Uniform Resource Indicators defined by rfc3986
    """
    scheme = None;
    authority = None;
    host = None;
    path = None;
    query_params = {};

    def __init__(self, uri=None):
        if uri != None:
            self.parse(uri)

    def parse(self, uri):
        """Parse the provided uri into the various components of a uri"""

        scheme_range = None
        # Grab the scheme (the part before the colon)
        if uri.find(":") >= 0:
            scheme_idx = uri.find(':')
            scheme_range = (0, scheme_idx,)
            self.scheme = uri[scheme_range[0]:scheme_range[1]]

        # Grab the authority, if we have one
        authority_range = None
        if uri.find("//") >= 0:
            authority_start_idx = uri.find("//") + 2 # account for the // characters
            authority_end_idx = -1
            # we have an authority, look for and ending (/, ?, #)
            if uri.find('/', authority_start_idx) >= 0:
                authority_end_idx = uri.find('/', authority_start_idx)
            elif uri.find('?', authority_start_idx) >= 0:
                authority_end_idx = uri.find('?', authority_start_idx)
            elif uri.find('#', authority_start_idx) >= 0:
                authority_end_idx = uri.find('#', authority_start_idx)
            else:
                authority_end_idx = len(uri)
            
            authority_range = (authority_start_idx, authority_end_idx,)
            self.authority = uri[authority_start_idx:authority_end_idx]

        # TODO: parse authority into user-spec, host, port - converting this properly
        #       requires being able to parse domain, IPv4, IPv6, users, ports
        #       authority   = [ userinfo "@" ] host [ ":" port ]
        #       userinfo    = *( unreserved / pct-encoded / sub-delims / ":" )
        #       host        = IP-literal / IPv4address / reg-name
        #       port        = *DIGIT
        self.host = self.authority

        # Parse out the path
        path_range = None
        
        # Check for authority, then scheme (authority always comes after scheme)
        path_start_idx = -1
        if authority_range != None:
            path_start_idx = authority_range[1]
        elif authority_range == None and scheme_range != None:
            path_start_idx = scheme_range[1] + 1 # account for the :
        # Check for naked path
        elif scheme_range == None and authority_range == None:
            path_start_idx = 0
         
        # Determine the path range if we have a place to start
        if path_start_idx >= 0:   
            # Calculate range
            if uri.find('?', path_start_idx) >= 0:
                path_range = (path_start_idx, uri.find('?', path_start_idx),)
            elif uri.find('#', path_start_idx) >= 0:
                path_range = (path_start_idx, uri.find('#', path_start_idx),)
            else:
                path_range = (path_start_idx, len(uri),)

        # Grab the path if we have a range to work with
        if path_range != None and path_range[0] != path_range[1]:
            self.path = uri[path_range[0]:path_range[1]]



    def __str__(self):
        uri_components = []
        if self.scheme != None:
            uri_components.append(self.scheme)
            uri_components.append(':')
        if self.authority != None:
            uri_components.append('//')
            uri_components.append(self.authority)
        if self.path != None:
            uri_components.append(self.path)

        query_indicated = False
        for k,v in self.query_params.iteritems():
            if not query_indicated:
                uri_components.append('?')
                query_indicated = True
            else:
                uri_components.append('&')
            uri_components.append(str(k))
            uri_components.append('=')
            uri_components.append(str(v)) # TODO: URL Encode
        return ''.join(uri_components)

        