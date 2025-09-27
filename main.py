import inspect
from typing import Any
from parse import parse
from response import Response
import types

SUPPORTED_METHODS = {'GET','POST','DELETE','PUT','PATCH'}

# def app(environ,start_response):
#     print(environ)
#     start_response('200 OK',headers = [])
#     return [b'Hello World'] #response is a string in byte format




class SlowAPI : 
    
    def __init__(self,middlewares = []) -> None : 
        self.routes = dict()
        self.middlewares = middlewares
        self.middleware_local = dict()

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
                    route_middlewares = self.middleware_local[path][request_method]
                    for mw in route_middlewares :
                        if isinstance(mw,types.FunctionType):
                            mw(environ)
                        else :
                            raise ValueError(" Middleware must be instance of function ")
                    handler(environ,response,**res.named)
                    return response.as_wsgi(start_response)
                
                    
        return response.as_wsgi(start_response) 


    def common_route(self, path, handler, method_name, middlewares = []) :
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

            # MIDDLEWARES
            #{
            #     '/users':{
            #         'GET' : [mw1,mw2]
            #         'POST' : [mw3,mw4]
            #     }
            # }
            if path_name not in self.middleware_local:
                self.middleware_local[path_name] = {}
            self.middleware_local[path_name][method_name] = middlewares

            print(self.routes) 


    def get(self,path=None,middlewares = []):
        def wrapper(handler):
            return self.common_route(path,handler,'GET',middlewares)   

        return wrapper  

    def post(self,path=None, middlewares = []):
        def wrapper(handler):
            return self.common_route(path,handler,'POST',middlewares)   

        return wrapper  

    def delete(self,path=None, middlewares = []):
        def wrapper(handler):
            return self.common_route(path,handler,'DELETE', middlewares)   

        return wrapper  
    

    def route(self,path = None , middlewares = []):
        def wrapper(handler):
            if isinstance(handler,type): #check if the handler is a class or not
                class_members = inspect.getmembers(handler,lambda x : inspect.isfunction(x) and not (
                    x.__name__.startswith('__') and x.__name__.endswith('__')) and x.__name__.upper() in SUPPORTED_METHODS
                )
                print(class_members)

                for f_name , f_handler in class_members :
                    self.common_route(path or f"/{handler.__name__}", f_handler , f_name.upper() ,  middlewares)

            else :
                raise ValueError("Handler must be a class")
            
        return wrapper

#making an instance of SlowAPI that will be called using the gunivorn gateway -> in example.py
#   slowapi = SlowAPI()