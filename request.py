from collections import defaultdict


class Request :
    def __init__(self,environ):
        self.queries = defaultdict()
        # defaultdict is used to avoid key error if the key is not present in the dictionary
        for key , value in environ.items():
            setattr(self,key.replace(".","_").lower(),value)

        if self.query_string :
            req_quaries = self.query_string.split('&')
            for quary in req_quaries :
                key , val = quary.split('=')
                self.queries[key] = val
                
