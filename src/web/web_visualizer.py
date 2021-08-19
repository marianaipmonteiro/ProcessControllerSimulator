import math
import threading

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.core.simulation import simulation

EXTERNAL_STYLESHEETS = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
NUM_SAMPLES_TO_DRAW = 100

NUM_GRAPHS_PER_ROW = 3

UPDATE_SPEED_SECONDS = 5


class WebVisualizer:
    def __init__(self, simulation: simulation):
        self.world_states = simulation.world_states
        self.lock = simulation.world_states_lock

        app = dash.Dash("Visualizer", external_stylesheets=EXTERNAL_STYLESHEETS)

        app.layout = html.Div(children=[
            html.H1(children='Data Visualizer'),
            dcc.Graph(
                id='output-graph'
            ),
            dcc.Interval(
                id='interval-component',
                interval=UPDATE_SPEED_SECONDS * 1000,
                n_intervals=0
            )
        ])

        @app.callback(Output('output-graph', 'figure'),
                      [Input('interval-component', 'n_intervals')])
        def update_line_graph(n):
            self.df = self.get_data_frame().tail(n=NUM_SAMPLES_TO_DRAW)
            num_graphs = len(self.df.columns)
            num_rows = int(math.ceil(num_graphs / NUM_GRAPHS_PER_ROW))

            subplot_titles = []
            for col_name in self.df.columns:
                if col_name != "Time":
                    subplot_titles.append(col_name + " over Time")

            fig = make_subplots(rows=num_rows, cols=NUM_GRAPHS_PER_ROW,
                                                shared_xaxes=True, subplot_titles=subplot_titles, vertical_spacing=0.2)

            counter = 0
            for col_name in self.df.columns:
                if col_name != "Time":
                    my_row = int(counter / NUM_GRAPHS_PER_ROW) + 1
                    my_col = counter % NUM_GRAPHS_PER_ROW + 1
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
            world_row.update({"Time": world.wall_clock_time.time().strftime('%H:%M:%S')})
            variables_list.append(world_row)
        df = pd.DataFrame(variables_list)
        return df

    def start(self):
        threading.Thread(target=self.start_server, args=()).start()

    def start_server(self):
        print("======== Starting server!")
        self.app.run_server(debug=False, dev_tools_silence_routes_logging=True, dev_tools_hot_reload=False)
