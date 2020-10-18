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

navbar = dbc.NavbarSimple(
    children=[],
    brand="whereishould.live",
    brand_href="#",
    color="dark",
    dark=True,
)