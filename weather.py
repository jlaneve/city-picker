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
import seaborn as sns

def render_precip(df, state, city):

    city_of_interest = df[(df['state_name_x'] == state) & (df['city'] == city)]
    index = city_of_interest.index[0]

    N = 50
    text = [str(df['LTM_mean_percipitation'].iloc[i])+', '+df['city'].iloc[i]+', '+df['state_name_x'].iloc[i] 
            for i in range(len(df))]
    size = [10 for i in range(len(text))]
    size[index] = 55

    fig = go.Figure()
    fig.add_trace(
        go.Scattergeo(
            locationmode = 'USA-states',
            lon = df['lng'], 
            lat = df['lat'],
            text = text,
            mode = 'markers',
            marker = dict(
                size = size,
                color=df['LTM_mean_percipitation'],
                opacity=0.75,
                colorscale = 'ice',
                colorbar = dict(
                    titleside = "right",
                    outlinecolor = "rgba(68, 68, 68, 0)",
                    ticks = "outside",
                    showticksuffix = "last",))))

    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ),
        title = 'USA by Long Term Mean Percipitation (mm)',
        showlegend = False,
        geo = dict(
            scope = 'north america',
            projection_type = 'albers usa',
            showland = True,
            landcolor = 'rgb(230,230,230)',
            countrycolor = 'rgb(204, 204, 204)'),
        width = 960*3/4, height = 700*3/4)

    return dcc.Graph(id = "precip-component", figure = fig, className="center-align")

def render_temp(df, state, city):

    city_of_interest = df[(df['state_name_x'] == state) & (df['city'] == city)]
    index = city_of_interest.index[0]

    N = 50
    colorscale = ['rgb'+str(i) for i in sns.color_palette("icefire", n_colors=N)]
    endpts = list(np.linspace(df['LTM_mean_temp'].min(), df['LTM_mean_temp'].max(), N-1))
    text = [str(df['LTM_mean_temp'].iloc[i])+', '+df['city'].iloc[i]+', '+df['state_name_x'].iloc[i] 
            for i in range(len(df))]
    size = [10 for i in range(len(text))]
    size[index] = 55

    fig = go.Figure()
    fig.add_trace(
        go.Scattergeo(
            locationmode = 'USA-states',
            lon = df['lng'], 
            lat = df['lat'],
            text = text,
            mode = 'markers',
            marker = dict(
                size = size,
                color=df['LTM_mean_temp'],
                opacity=0.75,
                colorscale = 'icefire',
                colorbar = dict(
                    titleside = "right",
                    outlinecolor = "rgba(68, 68, 68, 0)",
                    ticks = "outside",
                    showticksuffix = "last",))))

    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        ),
        title = 'USA by Long Term Mean Temperature (F°)',
        showlegend = False,
        geo = dict(
            scope = 'north america',
            projection_type = 'albers usa',
            showland = True,
            landcolor = 'rgb(230,230,230)',
            countrycolor = 'rgb(204, 204, 204)'),
        width = 960*3/4, height = 700*3/4)

    return dcc.Graph(id = "temp-component", figure = fig, className="center-align")