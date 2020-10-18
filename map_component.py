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

from single_city import make_city
from navbar import navbar
from search import make_form


def render_map(df):
    fig = go.Figure()

    fig.add_trace(
        go.Scattergeo(
            locationmode = 'USA-states',
            lon = df['lng'], 
            lat = df['lat'],
            text = df['city']+', '+df['state_name_x'],
            mode = 'markers',
            marker = dict(
                size = 30,
                color = 'rgb(0, 168, 194)',
                opacity=0.5,)
        )
    )   
        
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ),
        title = 'Recomended Cities',
        title_x=0.5,
        showlegend = False,
        geo = dict(
            scope = 'north america',
            projection_type = 'albers usa',
            showland = True,
            landcolor = 'rgb(230,230,230)',
            countrycolor = 'rgb(204, 204, 204)'),
        width = 960, height = 700
    )

    return dcc.Graph(id = "map-component", figure = fig, style = {'textAlign':'left', "display": "block", 'padding-left': 75, 'border-color': '#6c1420'})