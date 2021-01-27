import math
import threading
from typing import List

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from simulation import Simulation
from simulation.utils import wait_for_world_initialization

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


class Visualizer:
    def __init__(self, simulation: Simulation):
        self.world_states = simulation.world_states
        self.lock = simulation.world_states_lock

        wait_for_world_initialization(self.lock, self.world_states)

        app = dash.Dash("Visualizer", external_stylesheets=external_stylesheets)

        app.layout = html.Div(children=[
            html.H1(children='Data Visualizer'),

            dcc.Graph(
                id='output-graph'
            ),
            dcc.Interval(
                id='interval-component',
                interval=10 * 1000,
                n_intervals=0
            )
        ])

        @app.callback(Output('output-graph', 'figure'),
                      [Input('interval-component', 'n_intervals')])
        def update_line_graph(n):
            self.df = self.get_data_frame()
            num_graphs = len(self.df.columns)
            num_graphs_per_row = 3
            num_rows = int(math.ceil(num_graphs / num_graphs_per_row))

            subplot_titles = []
            for col_name in self.df.columns:
                if col_name != "Time":
                    subplot_titles.append(col_name + " over Time")

            fig = make_subplots(rows=num_rows, cols=num_graphs_per_row,
                                                shared_xaxes=True, subplot_titles=subplot_titles, vertical_spacing=0.2)

            counter = 0
            for col_name in self.df.columns:
                if col_name != "Time":
                    my_row = int(counter / num_graphs_per_row) + 1
                    my_col = counter % num_graphs_per_row + 1
                    fig.add_trace(go.Scatter(x=self.df["Time"], y=self.df[col_name]), row=my_row, col=my_col)
                    fig.update_xaxes(title_text="Time", row=my_row, col=my_col)
                    fig.update_yaxes(title_text=col_name, row=my_row, col=my_col)
                    counter += 1
            return fig

        self.app = app

    def get_data_frame(self):
        worlds = []
        self.lock.acquire()
        worlds = self.world_states.copy()
        self.lock.release()
        variables_list = []

        for world in worlds:
            world_row = world.variables.copy()
            world_row.update({"Time": world.wall_clock_time.time()})
            variables_list.append(world_row)
        df = pd.DataFrame(variables_list)
        return df

    def start(self):
        threading.Thread(target=self.start_server, args=()).start()

    def start_server(self):
        print("======== Starting server!")
        self.app.run_server(debug=False, dev_tools_silence_routes_logging=True, dev_tools_hot_reload=True)
