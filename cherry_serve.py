import cherrypy
from pos.wsgi import application

cherrypy.tree.graft(application, "/")

cherrypy.config.update({
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 8000,  # Change the port if needed
})

if __name__ == '__main__':
    cherrypy.engine.start()
    cherrypy.engine.block()
