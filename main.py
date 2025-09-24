from typing import Any
# def app(environ,start_response):
#     print(environ)
#     start_response('200 OK',headers = [])
#     return [b'Hello World'] #response is a string in byte format




class SlowAPI : 
    
    def __init__(self) -> None : 
        self.routes = dict()

    def __call__(self,environ,start_response) -> Any :
        response = {}
        for path,handler_dict in self.routes.items() :
            for request_method , handler in handler_dict.items() :
                if path == environ['PATH_INFO'] and request_method == environ['REQUEST_METHOD']:
                    handler(environ,response)
                    start_response(response['status_code'], response['headers'])
                    return [response['text'].encode()]



    def get(self,path=None):
        def wrapper(handler):
            # {
            #     '/users':{
            #         'GET' : handler
            #     }
            # }
            path_name = path or f"/{handler.__name__}"

            if path_name not in self.routes:
                self.routes[path_name] = {}
            self.routes[path_name]['GET'] = handler
            print(self.routes)    

        return wrapper  

#making an instance of SlowAPI that will be called using the gunivorn gateway -> in example.py
#   slowapi = SlowAPI()