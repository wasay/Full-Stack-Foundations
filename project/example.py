
                url = self.path

                parse_string = parse_qs(url)

                o = urlparse(url)

                output += ("<p>scheme: %s</p>") %  o.scheme
                output += ("<p>netloc: %s</p>") %  o.netloc
                output += ("<p>hostname: %s</p>") %  o.hostname
                output += ("<p>port: %s</p>") %  o.port
                output += ("<p>path: %s</p>") %  o.path
                output += ("<p>params: %s</p>") %  o.params
                output += ("<p>query: %s</p>") %  o.query
                output += ("<p>fragment: %s</p>") %  o.fragment
                output += ("<p>username: %s</p>") %  o.username
                output += ("<p>password: %s</p>") %  o.password

                output += ("<p>URL: %s</p>") % url
                output += ("<p>URL Parse1: %s</p>") % (parse_string)

                #query_string = parse_qs(urlparse(url).query, keep_blank_values=True)
                #output += ("<p>URL Parse2: %s</p>") % (query_string)