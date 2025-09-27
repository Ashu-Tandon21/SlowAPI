from main import SlowAPI
from response import Response


def global_middleware(request):
    print("This was executed before anything(route) \n")

def local_middleware(request):
    print("This was executed before the route handler \n")

slowapi = SlowAPI(middlewares=[global_middleware])


@slowapi.get("/users/{id}",middlewares = [local_middleware])
def get_users(req,res,id) :
    # res['status_code'] = '200 OK'
    # res['headers'] = []
    # res['text'] = "['Ashu','Ashutosh']"
    res.send(id,200)


# @slowapi.post('/users')
# def create_user(req,res) :
#     res.send("User Created",'201 Created')


@slowapi.route()
class User :
    def __init__(self):
        pass

    def get(req,res):
            res.send("Get all users")
        
    def post(req,res):
        res.send("Create a user",200)

    def helper(req,res):
        pass