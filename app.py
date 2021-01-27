#!/usr/bin/env python3.7

import pandas as pd
import datetime as dt
import json
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from clean_data import df_list, counties
