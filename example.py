from main import SlowAPI

slowapi = SlowAPI()

@slowapi.get('/users')
def get_users(req,res) :
    res['status_code'] = '200 OK'
    res['headers'] = []
    res['text'] = "['Ashu','Ashutosh']"