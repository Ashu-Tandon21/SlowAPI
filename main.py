from typing import Any
from parse import parse
from response import Response
import types
# def app(environ,start_response):
#     print(environ)
#     start_response('200 OK',headers = [])
#     return [b'Hello World'] #response is a string in byte format




class SlowAPI : 
    
    def __init__(self,middlewares = []) -> None : 
        self.routes = dict()
        self.middlewares = middlewares

    def __call__(self,environ,start_response) -> Any :
        response = Response()
        # ****************
        #dictionary is not suitable in this scinario as it does not maintain the order of insertion
        #plus we want to have multiple handlers for same path with different request methods
        # ****************
        '''
            checking if the middlewares are instance of function or not 
            as we want are global middlewares to be of instance of function 
        '''
        for middleware in self.middlewares :
            if isinstance(middleware,types.FunctionType):
                middleware(environ)
            else :
                raise ValueError(" Middleware must be instance of function ")

        for path,handler_dict in self.routes.items() :
            res = parse(path,environ['PATH_INFO'])
            
            for request_method , handler in handler_dict.items() :
                if res and request_method == environ['REQUEST_METHOD']:
                    handler(environ,response,**res.named)
                    return response.as_wsgi(start_response)
                    
        return response.as_wsgi(start_response) 


    def common_route(self, path, handler, method_name):
        # {
            #     '/users':{
            #         'GET' : handler
            #         'POST' : handler2
            #         'DELETE' : handler3
            #         'PUT' : handler4
            #         'PATCH' : handler5
            #     }
            # }
            path_name = path or f"/{handler.__name__}"

            if path_name not in self.routes:
                self.routes[path_name] = {}
            self.routes[path_name][method_name] = handler
            print(self.routes) 


    def get(self,path=None):
        def wrapper(handler):
            return self.common_route(path,handler,'GET')   

        return wrapper  

    def post(self,path=None):
        def wrapper(handler):
            return self.common_route(path,handler,'POST')   

        return wrapper  

    def delete(self,path=None):
        def wrapper(handler):
            return self.common_route(path,handler,'DELETE')   

        return wrapper  

#making an instance of SlowAPI that will be called using the gunivorn gateway -> in example.py
#   slowapi = SlowAPI()