from main import SlowAPI
from response import Response


def global_middleware(request):
    print("This was executed before anything(route) \n")

slowapi = SlowAPI(middlewares=[global_middleware])

@slowapi.get("/users/{id}")
def get_users(req,res,id) :
    # res['status_code'] = '200 OK'
    # res['headers'] = []
    # res['text'] = "['Ashu','Ashutosh']"
    res.send(id,200)


@slowapi.post('/users')
def create_user(req,res) :
    res.send("User Created",'201 Created')