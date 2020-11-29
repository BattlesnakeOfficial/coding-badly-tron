import os

import cherrypy

from snake import Battlesnake

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Server(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        snake = Battlesnake()
        return {
            "apiversion": snake.apiversion,
            "author": snake.author,
            "version": snake.version,
            "color": snake.color,
            "head": snake.head,
            "tail": snake.tail,
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        data = cherrypy.request.json
        move = Battlesnake().move(data)
        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        print("END")
        return "ok"


if __name__ == "__main__":
    server = Server()

    # cherrypy.log.screen = None
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {
            "server.socket_port": int(os.environ.get("PORT", "8080")),
        }
    )

    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
