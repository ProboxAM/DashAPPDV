# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from io import StringIO
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import csv
import pandas as pd
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

header_y = []

colors = {
    'background': '##E0F2F7',
    'section': '#F2F2F2',
    'plotcolor' : '#CEECF5',
    'text': '#151515'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_csv('hapiscore_whr.csv')
d2f = pd.read_csv('combined_set.csv')
all_continents = d2f.Continent.unique()

geojson = px.data.gapminder()

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Happiness rate around the world',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='''
        Marc Guillén and Axel Alavedra Dash practice for the Data visualization assignement.
        ''',
        style={
        'textAlign': 'center',
        'color': colors['text']
        }
    ),

    dcc.Slider(
        id='year_slider',
        min=2005,
        max=2019,
        marks={i: 'Year {}'.format(i) if i == 1 else str(i) for i in range(2005, 2020)},
        value=2005,        
    ),

    html.Div(children=[
        dcc.Graph(
            id='mapchart'
        ),

        dcc.Checklist(
            id="checklist",
            options=[{"label": x, "value": x} 
                    for x in all_continents],
            value = all_continents[1:2],
            labelStyle={'display': 'inline-block'}
        ),

        dcc.Dropdown(
            id="dropdown",
            options=[
                    {"label": "Life Ladder", "value": "Life Ladder"},
                    {"label": "Log GDP per capita", "value": "Log GDP per capita"},
                    {"label": "Social support", "value": "Social support"},
                    {"label": "Healthy life expectancy at birth", "value": "Healthy life expectancy at birth"},
                    {"label": "Freedom to make life choices", "value": "Freedom to make life choices"},
                    {"label": "Generosity", "value": "Generosity"},
                    {"label": "Perceptions of corruption", "value": "Perceptions of corruption"},
                    {"label": "Positive affect", "value": "Positive affect"},
                    {"label": "Negative affect", "value": "Negative affect"},
                    {"label": "Confidence in national government", "value": "Confidence in national government"},
                    {"label": "Democratic Quality", "value": "Democratic Quality"},
                    {"label": "Delivery Quality", "value": "Delivery Quality"},
                    {"label": "Gapminder Life Expectancy", "value": "Gapminder Life Expectancy"},
                ],
            value = 'Life Ladder',
            clearable = False
        ),

        dcc.Graph(
            id='linechart'
        ),

        dcc.Dropdown(
            id="xdropdown",
            options=[
                    {"label": "Life Ladder", "value": "Life Ladder"},
                    {"label": "Log GDP per capita", "value": "Log GDP per capita"},
                    {"label": "Social support", "value": "Social support"},
                    {"label": "Healthy life expectancy at birth", "value": "Healthy life expectancy at birth"},
                    {"label": "Freedom to make life choices", "value": "Freedom to make life choices"},
                    {"label": "Generosity", "value": "Generosity"},
                    {"label": "Perceptions of corruption", "value": "Perceptions of corruption"},
                    {"label": "Positive affect", "value": "Positive affect"},
                    {"label": "Negative affect", "value": "Negative affect"},
                    {"label": "Confidence in national government", "value": "Confidence in national government"},
                    {"label": "Democratic Quality", "value": "Democratic Quality"},
                    {"label": "Delivery Quality", "value": "Delivery Quality"},
                    {"label": "Gapminder Life Expectancy", "value": "Gapminder Life Expectancy"},
                ],
            value = 'Life Ladder',
            clearable = False
        ),

        dcc.Dropdown(
            id="ydropdown",
            options=[
                    {"label": "Life Ladder", "value": "Life Ladder"},
                    {"label": "Log GDP per capita", "value": "Log GDP per capita"},
                    {"label": "Social support", "value": "Social support"},
                    {"label": "Healthy life expectancy at birth", "value": "Healthy life expectancy at birth"},
                    {"label": "Freedom to make life choices", "value": "Freedom to make life choices"},
                    {"label": "Generosity", "value": "Generosity"},
                    {"label": "Perceptions of corruption", "value": "Perceptions of corruption"},
                    {"label": "Positive affect", "value": "Positive affect"},
                    {"label": "Negative affect", "value": "Negative affect"},
                    {"label": "Confidence in national government", "value": "Confidence in national government"},
                    {"label": "Democratic Quality", "value": "Democratic Quality"},
                    {"label": "Delivery Quality", "value": "Delivery Quality"},
                    {"label": "Gapminder Life Expectancy", "value": "Gapminder Life Expectancy"},
                ],
            value = 'Log GDP per capita',
            clearable = False
        ),

        dcc.Graph(
            id='bubblechart'
        )
    ])
])

@app.callback(
    Output('mapchart', 'figure'),
    Input('year_slider', 'value'))
def update_figure(selected_year):

    fig = px.choropleth(df, locations="country", locationmode="country names", hover_name="country", color=str(selected_year), title="Choropleth", fitbounds="locations")

    fig.update_layout(
        plot_bgcolor=colors['plotcolor'],
        paper_bgcolor=colors['section'],
        font_color=colors['text'],
    )

    return fig

@app.callback(
    Output('linechart', 'figure'),
    Input('checklist', 'value'),
    Input('dropdown', 'value')
    )
def update_figure(checklist, dropdown):
    mask = d2f.Continent.isin(checklist)
    fig = px.line(d2f[mask], x="Year", y=dropdown, color="Country name", title="Linechart")

    fig.update_layout(
        plot_bgcolor=colors['plotcolor'],
        paper_bgcolor=colors['section'],
        font_color=colors['text'],
    )

    return fig

@app.callback(
    Output('bubblechart', 'figure'),
    Input('ydropdown', 'value'),
    Input('xdropdown', 'value')
)
def update_figure(xdropdown, ydropdown):
    fig = px.scatter(d2f.query("Year==2007"), x=xdropdown, y=ydropdown,
        size="Gapminder Population", color="Continent",
        hover_name="Country name", log_x=True, size_max=60, title="Bubble Chart")

    fig.update_layout(
        plot_bgcolor=colors['plotcolor'],
        paper_bgcolor=colors['section'],
        font_color=colors['text'],
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)