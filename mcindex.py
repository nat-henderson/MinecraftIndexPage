import cherrypy
from mako.template import Template
from mako.lookup import TemplateLookup
from threading import Timer
from mcquery import MCQuery
from mcapi import MinecraftJsonApi
import time
import os
import pickle

F_NAME = ".index_props"
STATIC_DIR = '/home/minecraft/working_copy_indexpage/static'
lookup = TemplateLookup(directories=['html'])

class MCIndex:
    @cherrypy.expose
    def index(self):
        with open(F_NAME) as f: users = pickle.load(f)
        if os.path.getmtime(F_NAME) < time.time() - 20:
            status = "Down"
        else:
            status = "Up"
        tmpl = lookup.get_template("index.html")
        return tmpl.render(status = status, users = users)

def update_now_and_then_please():
    try:
        players = api_obj.call('getPlayers')
        attr_list = []
        for player in players:
            attr = []
            attr.append(player['name'])
            attr.append(player['level'])
            attr.append(player['location']['x'])
            attr.append(player['location']['y'])
            attr.append(player['location']['z'])
            attr.append(player['health'])
            attr_list.append(attr)
        print attr_list
        with open(F_NAME, 'w') as f: pickle.dump(attr_list, f)
        with open(STATIC_DIR + '/playerdata', 'w') as f:
            tmpl = lookup.get_template('playerdata.html')
            f.write(tmpl.render(users = attr_list))
    except IOError as e:
        print e
    t = Timer(10, update_now_and_then_please)
    t.start()

params = {'host': 'localhost', 'port':20059, 'username':'mcadmin', 'password':'correcthorsebatterystaple', 'salt':'nothinginterestingwhatsoeverisgoinghereatall'}

api_obj = MinecraftJsonApi(
         host = params['host'],
         port = params['port'],
         username = params['username'],
         password = params['password'],
         salt = params['salt']
     )

print 'serving...'

t = Timer(2, update_now_and_then_please)
t.start()

cherrypy.server.socket_host = '0.0.0.0'
config = {'/static':
    {   'tools.staticdir.on': True,
        'tools.staticdir.dir': STATIC_DIR,
    }
}

cherrypy.server.socket_port = 8080
cherrypy.tree.mount(MCIndex(), '/', config=config)
try:
    cherrypy.engine.start()
except KeyboardInterrupt:
    t.cancel()
    cherrypy.engine.stop()
