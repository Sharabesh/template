#!/usr/bin/python
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.websocket
import os
import requests
from socket import *
from constants import COOKIE_SECRET, PORT
from BaseHandler import BaseHandler
import sys

sys.path.append("auth")
from auth.validation_endpoints import LogoutHandler, LoginHandler, UserSignupHandler


class MainHandler(BaseHandler):
    def get(self):
        self.render("templates/html/main.html")


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("Opened Socket")

    def on_message(self, message):
        print(message)
        to_search = message.replace(" ", "+")
        goog_search = (
            "https://www.google.co.uk/search?sclient=psy-ab&client=ubuntu&hs=k5b&channel=fs&biw=1366&bih=648&noj=1&q="
            + to_search
        )
        r = requests.get(goog_search)
        self.write("HELLO WORLD")

    def on_close(self):
        print("Closed Socket")


settings = {
    "login_url": "/login",
    "compress_reponse": True,
    "cookie_secret": COOKIE_SECRET,
}


def make_app():
    return tornado.web.Application(
        [
            (
                r"/static/(.*)",
                tornado.web.StaticFileHandler,
                {
                    "path": os.path.join(
                        os.path.dirname(os.path.abspath(__file__)), "static"
                    )
                },
            ),
            (r"/", MainHandler),
            (r"/websocket", WebSocketHandler),
            (r"/login", LoginHandler),
            (r"/login", LogoutHandler),
            (r"/signup", UserSignupHandler),
        ],
        debug=True,
        compress_response=True,
        **settings,
    )


if __name__ == "__main__":
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)

    port = int(os.environ.get("PORT", PORT))
    http_server.listen(port)

    print(f"Running at localhost:{port}")
    tornado.ioloop.IOLoop.current().start()
