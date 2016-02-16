# -*- coding: utf-8 -*-
from tornado import ioloop, websocket
from tornado.web import RequestHandler, Application


class EchoWebSocket(websocket.WebSocketHandler):
    sockets = []

    def check_origin(self, origin):
        return True

    def open(self):
        print("WebSocket opened")
        self.sockets.append(self)
        print(self.sockets)

    def on_message(self, message):
        self.write_message(u"You said: " + message)
        for s in self.sockets:
            s.write_message(message)

    def on_close(self):
        print("WebSocket closed")


class MessageHandler(RequestHandler):
    def get(self, pk=None):
        if not pk:
            self.write('all messages')
            self.flush()


if __name__ == '__main__':
    app = Application([
        (r'/', MessageHandler),
        (r'/test/', MessageHandler),
        (r'/websocket/?', EchoWebSocket),
    ])
    app.listen(8899, '127.0.0.1')
    print('Start')
    ioloop.IOLoop.current().start()
