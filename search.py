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

def make_select_component(title, opts, id):
    return dbc.FormGroup(
        [
            dbc.Label(title),
            dbc.Select(
                id=id,
                options=opts,
            ),
        ]
    )

params = [
    {
        "title": "Size",
        "id": "size",
        "opts": [
            {"label": "I want a Small city", "value": "low"},
            {"label": "I want a Medium city", "value": "medium"},
            {"label": "I want a Large city", "value": "high"},
            {"label": "Give me an Extremely large city!", "value": "highest"}
        ]
    },
    {
        "title": "Diversity",
        "id": "diversity",
        "opts": [
            {"label": "Very Diverse", "value": "high"},
            {"label": "Average Diversity", "value": "medium"},
            {"label": "Low Diversity", "value": "low"},
        ]
    },
    {
        "title": "Education",
        "id": "education",
        "opts": [
            {"label": "High Number of HS/College Grads", "value": "high"},
            {"label": "Average Graduation Levels", "value": "medium"},
            {"label": "Low HS/College Graduation Rates", "value": "low"},
        ]
    },
    {
        "title": "Wealth",
        "id": "wealth",
        "opts": [
            {"label": "Upper Income Bracket", "value": "high"},
            {"label": "Middle Income Bracket", "value": "medium"},
            {"label": "Lower Income Bracket", "value": "low"},
        ]
    },

    {
        "title": "Home Price",
        "id": "home_price",
        "opts": [
            {"label": "High", "value": "high"},
            {"label": "Medium", "value": "medium"},
            {"label": "Low", "value": "low"},
        ]
    },
    
    {
        "title": "I Prefer Weather That's",
        "id": "weather",
        "opts": [
            {"label": "Hot", "value": "high"},
            {"label": "Temperate", "value": "medium"},
            {"label": "Cold", "value": "low"},
        ]
    },

    {
        "title": "COVID-19 Response",
        "id": "covid",
        "opts": [
            {"label": "Highly-Successful (low COVID cases & deaths)", "value": "high"},
            {"label": "Average COVID response", "value": "medium"},
            {"label": "Poor COVID response (high COVID cases & deaths)", "value": "low"},
        ]
    },

    {
        "title": "Professional Opportunities",
        "id": "profession",
        "opts": [
            {"label": "High", "value": "high"},
            {"label": "Medium", "value": "medium"},
            {"label": "Low", "value": "low"},
        ]
    },
    
    {
        "title": "How Do I Feel About Public Transit?",
        "id": "transit",
        "opts": [
            {"label": "Need it", "value": "highest"},
            {"label": "Like it", "value": "high"},
            {"label": "Indifferent", "value": "medium"},
            {"label": "Hate It", "value": "low"},
        ]
    },

    {
        "title": "Poverty Rates",
        "id": "poverty",
        "opts": [
            {"label": "Low Poverty Rates", "value": "high"},
            {"label": "Average Poverty Rates", "value": "medium"},
            {"label": "High Poverty Rates", "value": "low"},
        ]
    },
    
    {
        "title": "I Prefer a Population That Is",
        "id": "age",
        "opts": [
            {"label": "Younger", "value": "high"},
            {"label": "Average Aged", "value": "medium"},
            {"label": "Older", "value": "low"},
        ]
    },
]


def make_form():
    return html.Div(children=[
        html.Div(children=[
            html.Div(
                    make_select_component(param["title"], param["opts"], param["id"]),
            className="col-sm-4") for param in params
        ], className="row")
    ])