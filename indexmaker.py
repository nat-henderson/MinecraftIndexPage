from cherrypy import wsgiserver
from mcquery import MCQuery
from threading import Timer
import pickle
import time

F_NAME = '.index_props'

def hello_world_app(environ, start_response):
    t_0 = time.time()
    status = '200 OK' # HTTP Status
    headers = [('Content-type', 'text/plain')] # HTTP Headers
    start_response(status, headers)
    with open(F_NAME) as f: response = pickle.load(f)
    print time.time() - t_0
    if 'players' in response:
        n_players = len(response['players'])
        # The returned object is going to be printed
        return "Server up with " + str(n_players) + " players."
    else:
        return "Server down."

def update_now_and_then_please():
    try:
        query_obj = MCQuery('localhost', 25565)
        response = query_obj.full_stat()
    except IOError:
        response = "Server down"
    with open(F_NAME, 'w') as f: pickle.dump(response, f)
    t = Timer(20, update_now_and_then_please)
    t.start()

t = Timer(2, update_now_and_then_please)
t.start()
server = wsgiserver.CherryPyWSGIServer(('0.0.0.0', 8000), hello_world_app, server_name = 'localhost')
print "Serving on port 8000..."

# Serve until process is killed
try:
    server.start()
except KeyboardInterrupt:
    server.stop()
