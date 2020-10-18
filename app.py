# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

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
from map_component import render_map


print("SERVER STARTED")


# DATA
df = pd.read_csv("./data/df.csv")
transf = pd.read_csv("./data/transf.csv")
centroids = pd.read_csv("./data/column_centroids.csv")
city_info = pd.read_csv("./data/city_info.csv")
feature_vectors = pd.read_csv("./data/feature_vectors.csv")
danger_over_time = pd.read_csv("./data/danger_over_time.csv")


app = dash.Dash(__name__, external_stylesheets=["https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css"], external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js"])
app.title = "City Picker"
server = app.server

def recommendations(user, num_recs=20):
    
    """
    Returns the top num_recs recommendations for a given feature vector

    Parameters:
        - user: the user vector
        - num_recs: the number of recommendations to return (default: 15)

    Returns:
        - A list of ranked cities and states

    """
    
    current_recs = 0
    i = 0
    list_recs = []
    d = { 'similarity' : [np.dot(feature_vectors.values[i, 0:13], user) for i in range(100)]}
    similarity = pd.DataFrame(data=d)
    similarity['clusterId'] = similarity.index
    similarity = similarity.sort_values(by='similarity', ascending=False)

    data = pd.DataFrame(city_info[['city', 'state_id', 'clusterId']])

    while(current_recs < num_recs):
        cluster = data[data['clusterId'] == similarity['clusterId'].iloc[i]][['city', 'state_id']]
        for k in range(cluster.shape[0]):
            list_recs.append(cluster.iloc[k, :].values)
        
        i = i + 1
        current_recs = len(list_recs)

    
    return list_recs[0:num_recs]

def make_feature_vector(size_filter, diversity_filter,
    education_filter, wealth_filter, home_price_filter, weather_filter, covid_filter,
    profession_filter, transit_filter, poverty_filter, age_filter):
    feature_vector = np.zeros(13)

    if size_filter:
        normalized_center = centroids[(centroids["feature"] == "size") & (centroids["group_name"] == size_filter)].iloc[0]["center_normalized"]
        feature_vector[0] = normalized_center

    if diversity_filter:
        normalized_center = centroids[(centroids["feature"] == "diversity") & (centroids["group_name"] == diversity_filter)].iloc[0]["center_normalized"]
        feature_vector[1] = normalized_center

    if education_filter:
        normalized_center = centroids[(centroids["feature"] == "education") & (centroids["group_name"] == education_filter)].iloc[0]["center_normalized"]
        feature_vector[2] = normalized_center

    if wealth_filter:
        normalized_center = centroids[(centroids["feature"] == "wealth") & (centroids["group_name"] == wealth_filter)].iloc[0]["center_normalized"]
        feature_vector[3] = normalized_center
    
    if home_price_filter:
        normalized_center = centroids[(centroids["feature"] == "home_price") & (centroids["group_name"] == home_price_filter)].iloc[0]["center_normalized"]
        feature_vector[4] = normalized_center

    if weather_filter:
        normalized_center = centroids[(centroids["feature"] == "weather") & (centroids["group_name"] == weather_filter)].iloc[0]["center_normalized"]
        feature_vector[7] = normalized_center

    if covid_filter:
        normalized_center = centroids[(centroids["feature"] == "covid") & (centroids["group_name"] == covid_filter)].iloc[0]["center_normalized"]
        feature_vector[8] = normalized_center

    if profession_filter:
        normalized_center = centroids[(centroids["feature"] == "profession") & (centroids["group_name"] == profession_filter)].iloc[0]["center_normalized"]
        feature_vector[9] = normalized_center

    if transit_filter:
        normalized_center = centroids[(centroids["feature"] == "transit") & (centroids["group_name"] == transit_filter)].iloc[0]["center_normalized"]
        feature_vector[10] = normalized_center

    if poverty_filter:
        normalized_center = centroids[(centroids["feature"] == "poverty") & (centroids["group_name"] == poverty_filter)].iloc[0]["center_normalized"]
        feature_vector[11] = normalized_center

    if age_filter:
        normalized_center = centroids[(centroids["feature"] == "age") & (centroids["group_name"] == age_filter)].iloc[0]["center_normalized"]
        feature_vector[12] = normalized_center

    if np.sum(feature_vector) == 0:
        feature_vector = np.random.randint(-1, 1, size = 13)

    return feature_vector

@app.callback(Output(component_id="cities-list", component_property="children"), [
    Input(component_id="size", component_property="value"),
    Input(component_id="diversity", component_property="value"),
    Input(component_id="education", component_property="value"),
    Input(component_id="wealth", component_property="value"),
    Input(component_id="home_price", component_property="value"),
    Input(component_id="weather", component_property="value"),
    Input(component_id="covid", component_property="value"),
    Input(component_id="profession", component_property="value"),
    Input(component_id="transit", component_property="value"),
    Input(component_id="poverty", component_property="value"),
    Input(component_id="age", component_property="value"),
])
def update_list(size_filter, diversity_filter, education_filter,
    wealth_filter, home_price_filter, weather_filter, covid_filter, profession_filter, transit_filter,
    poverty_filter, age_filter):
    user_vector = make_feature_vector(size_filter, diversity_filter,
            education_filter, wealth_filter, home_price_filter, weather_filter,
            covid_filter, profession_filter, transit_filter, poverty_filter, age_filter)

    print(user_vector)
    
    recommends = [",".join(x) for x in recommendations(user_vector)]

    filtered_df = df[(df["city"] + "," + df["state_id"]).isin(recommends)]

    return html.Div(children=[
        render_map(filtered_df),
        html.Div([
            html.Div(make_city(row, danger_over_time, size_filter, diversity_filter, education_filter,
                wealth_filter, home_price_filter, weather_filter, covid_filter, profession_filter, transit_filter,
                poverty_filter, age_filter, df)) for i, row in filtered_df.iloc[0:5].iterrows()
        ])
    ])


def make_layout():
    return html.Div(children=[
        navbar,

        html.Div(children=[    
            html.H1(
                "City Picker!",
                style={
                    'textAlign': 'center',
                    'marginTop': '20px'
                }
            ),

            html.Br(),
            make_form(),
            html.Br(),

            html.Div(id="cities-list"),
        ], className="container"),
    ], className="target")

app.layout = make_layout

if __name__ == '__main__':
    app.run_server(debug=True)