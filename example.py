from main import SlowAPI
from response import Response

slowapi = SlowAPI()

@slowapi.get('/users')
def get_users(req,res) :
    # res['status_code'] = '200 OK'
    # res['headers'] = []
    # res['text'] = "['Ashu','Ashutosh']"
    res.send("['Ashu','Ashutosh']",'200')


@slowapi.post('/users')
def create_user(req,res) :
    res.send("User Created",'201 Created')