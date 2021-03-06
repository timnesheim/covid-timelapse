#!/usr/bin/env python3.7

import pandas as pd
import datetime as dt
import json
import plotly.graph_objects as go
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from clean_data import cases_df, counties

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    html.Div(
        dcc.Dropdown(
            id='xaxis-column',
            options=[{'label':i, 'value':i} for i in ['Cases','Deaths']],
            value='Cases'
        )
    ),

    html.H1(id='headline'),

    html.Div([
        dcc.Graph(
            id='fig-map'
        )
    ]),

    html.Div([
        dcc.Slider(
            id='fig-slider',
            min=cases_df['group_id'].min(),
            max=cases_df['group_id'].max(),
            value=cases_df['group_id'].min(),
        ),
        html.Div(id='fig-slider-container')
    ])
])

@app.callback(
    Output('headline','children'),
    [Input('xaxis-column','value')]
)
def get_headline(value):
    return 'Total {} by County'.format(value)

@app.callback(
    Output('fig-slider-container','children'),
    Input('fig-slider','value')
)
def display_date(value):
    dt = cases_df['date'].loc[cases_df['group_id'] == value].unique()[0]
    formatted_dt = dt.strftime('%a. %b %d, %Y')
    return 'Date: {}'.format(formatted_dt)


# TODO: find way to dynamically create map
@app.callback(
    Output('fig-map','figure'),
    [Input('fig-slider','value'),
     Input('xaxis-column','value')]
)
def display_figure(fig_slider_val,xaxis_column_val):

    df = cases_df[cases_df['group_id'] == fig_slider_val]

    col = df['cases_total'] if xaxis_column_val == 'Cases' else df['deaths_total']

    fig = go.Figure(data=go.Choropleth(
        locations=df['fips_updated'],
        geojson=counties,
        z=col,
        zmax=col.max(),
        zmin=col.min(),
    ))

    print(df)

    fig.update_layout(geo_scope='usa')

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
