import math
import threading

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from flask import Flask
from plotly.subplots import make_subplots

from src.core.simulation.simulation import Simulation

EXTERNAL_STYLESHEETS = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
NUM_SAMPLES_TO_DRAW = 100

NUM_GRAPHS_PER_ROW = 4

UPDATE_SPEED_SECONDS = 5


class WebVisualizer:
    def __init__(self, sim: Simulation, server: Flask):
        self.world_states = sim.world_states
        self.lock = sim.world_states_lock

        app = dash.Dash("Visualizer", server=server, url_base_pathname="/visualize/",external_stylesheets=EXTERNAL_STYLESHEETS)

        app.layout = html.Div(children=[
            html.H1(children='Data Visualizer'),
            dcc.Graph(
                id='output-graph'
            ),
            dcc.Interval(
                id='interval-component',
                interval=UPDATE_SPEED_SECONDS * 1000
            )
        ])

        @app.callback(Output('output-graph', 'figure'),
                      [Input('interval-component', 'n_intervals')])
        def render_variable_plots(n):
            df = self.get_data_frame()
            num_graphs = len(df.columns)
            num_rows = int(math.ceil(num_graphs / NUM_GRAPHS_PER_ROW))

            subplot_titles = []
            for col_name in df.columns:
                if col_name != "Time":
                    subplot_titles.append(col_name + " over Time")

            fig = make_subplots(rows=num_rows, cols=NUM_GRAPHS_PER_ROW,
                                shared_xaxes=True, subplot_titles=subplot_titles, vertical_spacing=0.2)
            fig.update_layout(showlegend=False)

            counter = 0
            for col_name in df.columns:
                if col_name != "Time":
                    my_row = int(counter / NUM_GRAPHS_PER_ROW) + 1
                    my_col = counter % NUM_GRAPHS_PER_ROW + 1
                    fig.add_trace(go.Scatter(x=df["Time"], y=df[col_name]), row=my_row, col=my_col)
                    fig.update_xaxes(title_text="Time", row=my_row, col=my_col)
                    fig.update_yaxes(title_text=col_name, row=my_row, col=my_col)
                    counter += 1
            return fig

        self.app = app

    def get_data_frame(self):
        self.lock.acquire()
        worlds = self.world_states[-NUM_SAMPLES_TO_DRAW:].copy()
        self.lock.release()

        table = []
        for w in worlds:
            var_copy = w.variables.copy()
            var_copy.update({"Time": w.wall_clock_time.time().strftime('%H:%M:%S')})
            table.append(var_copy)
        df = pd.DataFrame(table)
        return df

