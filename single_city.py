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
import wikipedia


def make_gender_chart(raw_genders):
    genders = raw_genders
    genders.name = "percentage"
    genders = pd.DataFrame(genders).reset_index()

    genders["gender"] = genders["index"].apply(lambda x: x.split("_")[1])
    fig = px.pie(genders, values = "percentage", names = "gender", title = "Gender composition")

    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.01
    ))

    return fig

def make_races_chart(raw_races):
    races = raw_races
    races.name = "percentage"
    races = pd.DataFrame(races).reset_index()

    races["ethnicity"] = races["index"].apply(lambda x: x.split("_")[1])
    fig = px.bar(races, y = "percentage", x = "ethnicity", color = "ethnicity", title = "Ethnicity composition")

    return fig

def make_unemployment_chart(unemployment_rate):
    rates = pd.DataFrame.from_dict({
        "unemployed": [unemployment_rate],
        "employed": [100 - unemployment_rate],
    }, orient="index", columns = ["percentage"]).reset_index().rename(columns = {"index": "category"})

    fig = px.pie(rates, values = "percentage", names = "category", title = "Employment rates")

    fig.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="right",
        x=0.01
    ))

    return fig

pop_dem_tab = lambda row: dbc.Card(
    dbc.CardBody([
        # Title
        html.Div("Population & Demographics", className="content-title"),

        # Total population
        html.Div("Total population: " + str(row["city_population"]), className="align-center"),

        html.Hr(),

        # Gender graph
        dcc.Graph(
            id = "gender",
            figure = make_gender_chart(
                row[["pct_men", "pct_women"]]
            ),
            className="center-align"
        ),

        # Ethnicities graph
        dcc.Graph(
            id = "ethnicity",
            figure = make_races_chart(
                row[["pct_hispanic", "pct_white", "pct_black", "pct_native", "pct_asian", "pct_pacific"]]
            ),
            className="center-align"
        ),

        # Unemployment graph
        dcc.Graph(
            id = "unemployment",
            figure = make_unemployment_chart(
                row["pct_unemployed"]
            ),
            className="center-align"
        ),
    ])
)

safety_tab = lambda row: dbc.Card(
    dbc.CardBody([
        html.Div("Public Safety Statistics", className="content-title"),

        html.Hr(),
    ])
)

def badges(row, size_filter, diversity_filter, education_filter,
    wealth_filter, home_price_filter, weather_filter, covid_filter, profession_filter, transit_filter,
    poverty_filter, age_filter):
    els = []

    if size_filter:
        els.append(
            dbc.Badge("Ranked #{} in population".format(int(row["size_rank"])), color="info", className="ml-1 float-right")
        )

    if diversity_filter:
        if diversity_filter == "high":
            els.append(
                dbc.Badge("Ranked #{} in most diverse cities".format(int(row["diversity_rank"])), color="info", className="ml-1 float-right")
            )
        if diversity_filter == "low":
            els.append(
                dbc.Badge("Ranked #{} in most diverse cities".format(int(row["diversity_rank"])), color="info", className="ml-1 float-right")
            )
    if education_filter:
        if education_filter == "high":
            els.append(
                dbc.Badge("Ranked #{} in best education cities".format(int(row["education_rank"])), color="info", className="ml-1 float-right")
            )
    if wealth_filter:
        if wealth_filter == "high":
            els.append(
                dbc.Badge("Ranked #{} in highest per capita income cities".format(int(row["wealth_rank"])), color="info", className="ml-1 float-right")
            )
    if home_price_filter:
        if home_price_filter == "high":
            els.append(
                dbc.Badge("Ranked #{} most expensive housing".format(int(row["home_price_rank"])), color="info", className="ml-1 float-right")
            )
    if covid_filter:
        if covid_filter == "low":
            els.append(
                dbc.Badge("Ranked #{} in worst covid response".format(791-int(row["covid_rank"])), color="info", className="ml-1 float-right")
            )
    if transit_filter:
        if transit_filter == "highest":
            els.append(
                dbc.Badge("Ranked #{} most used transit".format(int(row["transit_rank"])), color="info", className="ml-1 float-right")
            )
    if poverty_filter:
        if poverty_filter == "low":
            els.append(
                dbc.Badge("Ranked #{} in worst Poverty rates".format(int(row["poverty_rank"])), color="info", className="ml-1 float-right")
            )

    return els

def make_city(row, crime_over_time, size_filter, diversity_filter, education_filter,
    wealth_filter, home_price_filter, weather_filter, covid_filter, profession_filter, transit_filter,
    poverty_filter, age_filter, eid = None):
    if eid == None:
        eid = row.name

    # Find wikipedia content
    summary = row["wikipedia_summary"]

    return html.Div(children=[
        dbc.Card(children=[
            # Title
            dbc.CardHeader(children=[
                html.Span(html.B(row["city"])), html.Span(", " + row["state_id"]),

                html.Span(badges(row, size_filter, diversity_filter, education_filter,
                    wealth_filter, home_price_filter, weather_filter, covid_filter, profession_filter, transit_filter,
                    poverty_filter, age_filter))
            ]),


            dbc.CardBody([
                html.P(summary, style={"paddingBottom": "5px", "textIndent": "25px"}),
                dbc.Tabs([
                    dbc.Tab("", label="PICK A TAB ->"),
                    dbc.Tab(pop_dem_tab(row), label="POP & DEM"),
                    dbc.Tab(safety_tab(crime_over_time), label="SAFETY"),
                    dbc.Tab(filler_tab(row), label="Tab 3"),
                ])
            ]),
        ], className="mb-3",),
    ], className="city-card")