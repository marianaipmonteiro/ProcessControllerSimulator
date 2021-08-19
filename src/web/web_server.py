import threading

from flask import Flask


class WebServer:

    def __init__(self, name="web", host="0.0.0.0", port=8050, debug=False):
        self.host = host
        self.port = port
        self.debug = debug

        self.flask_app = Flask(name)

        @self.flask_app.route("/")
        def hello_world():
            return "Hellow, World!"

    def start(self):
        threading.Thread(target=self._run, args=()).start()
        #self._run()

    def _run(self):
        self.flask_app.run(host=self.host, port=self.port, debug=self.debug)
