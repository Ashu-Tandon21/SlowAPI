class Response :

    def __init__(self,status_code = '404 not found',text = 'Route not found') -> None:
        self.status_code = status_code
        self.headers = []
        self.text = text

    def as_wsgi(self,start_response) :
        start_response(self.status_code, headers = self.headers)

    def send(self,text = "",status_code = "200 OK") :
        if isinstance(text,str):
            self.text = text
        else :
            self.text = str(text) # we are converting whatever the uer is 
                                  #providing to string if it is not a string

        if isinstance(status_code,int):
            self.status_code = int(status_code)
        elif isinstance(status_code,str):
            self.status_code = status_code
        else :
            raise ValueError(" Status code must be either string or integer ")

        
        