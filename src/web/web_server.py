import threading

from flask import Flask, url_for, redirect, render_template
from flask_bootstrap import Bootstrap
from src import Simulation
from collections import namedtuple

from src.web.web_visualizer import WebVisualizer

NavItem = namedtuple("NavItem", ["name", "href", "html"])
home_nav = NavItem("Home", "/home/", "home.html")
howto_nav = NavItem("How To", "/how/", "how-to.html")
define_nav = NavItem("Define", "/define/", "define.html")
simulate_nav = NavItem("Simulate", "/simulate/", "simulate.html")
visualize_nav = NavItem("Visualize", "/visualize/", "visualize.html")  # NOTE: Dash will populate this page


class WebServer:

    def __init__(self, default_sim: Simulation, name="web", host="0.0.0.0", port=8050, debug=False):
        self.host = host
        self.port = port
        self.debug = debug
        self.simulations = {"default": default_sim}

        self.nav_items = [home_nav, howto_nav, define_nav, simulate_nav, visualize_nav]

        self.flask_app = Flask(name)
        self.flask_app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'flatly'
        self.bootstrap = Bootstrap(self.flask_app)

        self.dash_app = WebVisualizer(self.simulations["default"], self.flask_app)

        with self.flask_app.app_context():

            @self.flask_app.route("/")
            def root():
                return redirect(url_for("home"))

            @self.flask_app.route(home_nav.href)
            def home():
                return render_template(home_nav.html, simulations=self.simulations, bootstrap=self.bootstrap,
                                       nav_items=self.nav_items)

            @self.flask_app.route(howto_nav.href)
            def howto():
                return render_template(howto_nav.html, bootstrap=self.bootstrap, nav_items=self.nav_items)

            @self.flask_app.route(define_nav.href)
            def define():
                return render_template(define_nav.html, bootstrap=self.bootstrap, nav_items=self.nav_items)

            @self.flask_app.route(simulate_nav.href)
            def simulate():
                return render_template(simulate_nav.html, bootstrap=self.bootstrap, nav_items=self.nav_items)

            @self.flask_app.route(visualize_nav.href)
            def visualize():
                return render_template(visualize_nav.html, bootstrap=self.bootstrap, nav_items=self.nav_items, viz_name="default")



    def start(self):
        if self.debug:
            self._run()
        else:
            threading.Thread(target=self._run, args=()).start()
        # self._run()

    def _run(self):
        self.flask_app.run(host=self.host, port=self.port, debug=self.debug)
