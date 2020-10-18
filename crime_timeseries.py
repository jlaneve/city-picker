import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# takes as input like this df[df['state_name_x'] == 'Texas'] where df is the danger_over_time.csv

def render_crime(df):
    fig = go.Figure()

    for c in df['city'].unique():

        fig.add_trace(go.Scatter(
                        x = df[df['city'] == c]['year'],
                        y = df[df['city'] == c]['danger'],
                        name = c,
                        opacity=.9))

    fig.update_layout(title = 'Aggregate Crime Rate Over Time',
                    xaxis_range=[
                        df['year'].min(),
                        df['year'].max()
                    ],
                    width = 950, height = 600)
    color = 'rgb(209, 209, 209)'
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=color)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=color)

    return dcc.Graph(id = "crime-component", figure = fig)