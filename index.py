# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from io import StringIO
from os import link
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components.Br import Br
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
    'plotcolor': '#CEECF5',
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
        children='Country metrics around the globe',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='''
        This visualization explores different metrics of each country in the world during the last years, allowing the user to discover and explore. It contains a cholorphyte world map of the happiness that can be adjusted to show the data of each year. A line chart where the user can select different continents and compare the countries selected metric development over the years. Finally a big scatterplot where the user can select the year and both metrics to plot, to easily compare the countries.''',
             style={
                 'textAlign': 'center',
                 'color': colors['text']
             }
             ),

    html.Div(children=[
        html.P("Source: "),
        html.A("FBosler data ",
               "https://raw.githubusercontent.com/FBosler/AdvancedPlotting/master/combined_set.csv"),
        html.Br(),
        html.A("GapMinder data ", "https://docs.google.com/spreadsheets/d/1s4ryFpYS1AQAhI2E1XaQyZ0ikj6oF8YlwISrKkyNj6c/edit#gid=501532268"),
    ]),

    html.Br(),

    html.Div(children=[

        html.Br(),

        html.Div(
            style={
                'background': '#f2f2f2'
            },
            children=[html.Br(), html.H2(
                children = "CHOROPLETH",
                style={
                    'border' : '50px',
                    'textAlign': 'center',
                    'border-radius': 25,
                    'color': colors['text']
                }
            ), html.Br()]
        ),

        html.Br(),

        dcc.Checklist(
            id="checklist",
            options=[{"label": x, "value": x}
                     for x in all_continents],
            value=all_continents[1:2],
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(
            id='mapchart'
        ),

        dcc.Slider(
            id='year_slider',
            min=2005,
            max=2019,
            marks={i: 'Year {}'.format(i) if i == 1 else str(i)
                   for i in range(2005, 2020)},
            value=2005,
        ),

        html.Br(),

        html.Div(
            style={
                'background': '#f2f2f2'
            },
            children=[html.Br(), html.H2(
                children = "LINE CHART",
                style={
                    'border' : '50px',
                    'textAlign': 'center',
                    'color': colors['text']
                }
            ), html.Br()]
        ),

        html.Br(),

        dcc.Dropdown(
            id="dropdown",
            options=[
                {"label": "Life Ladder", "value": "Life Ladder"},
                {"label": "Log GDP per capita", "value": "Log GDP per capita"},
                {"label": "Social support", "value": "Social support"},
                {"label": "Healthy life expectancy at birth",
                    "value": "Healthy life expectancy at birth"},
                {"label": "Freedom to make life choices",
                    "value": "Freedom to make life choices"},
                {"label": "Generosity", "value": "Generosity"},
                {"label": "Perceptions of corruption",
                    "value": "Perceptions of corruption"},
                {"label": "Positive affect", "value": "Positive affect"},
                {"label": "Negative affect", "value": "Negative affect"},
                {"label": "Confidence in national government",
                    "value": "Confidence in national government"},
                {"label": "Democratic Quality", "value": "Democratic Quality"},
                {"label": "Delivery Quality", "value": "Delivery Quality"},
                {"label": "Gapminder Life Expectancy",
                    "value": "Gapminder Life Expectancy"},
            ],
            value='Life Ladder',
            clearable=False
        ),

        dcc.Graph(
            id='linechart'
        ),

        html.Br(),

        html.Div(
            style={
                'background': '#f2f2f2'
            },
            children=[html.Br(), html.H2(
                children = "BUBBLE CHART",
                style={
                    'border' : '50px',
                    'textAlign': 'center',
                    'color': colors['text']
                }
            ), html.Br()]
        ),

        html.Br(),

        dcc.Dropdown(
            id="xdropdown",
            options=[
                {"label": "Life Ladder", "value": "Life Ladder"},
                {"label": "Log GDP per capita", "value": "Log GDP per capita"},
                {"label": "Social support", "value": "Social support"},
                {"label": "Healthy life expectancy at birth",
                    "value": "Healthy life expectancy at birth"},
                {"label": "Freedom to make life choices",
                    "value": "Freedom to make life choices"},
                {"label": "Generosity", "value": "Generosity"},
                {"label": "Perceptions of corruption",
                    "value": "Perceptions of corruption"},
                {"label": "Positive affect", "value": "Positive affect"},
                {"label": "Negative affect", "value": "Negative affect"},
                {"label": "Confidence in national government",
                    "value": "Confidence in national government"},
                {"label": "Democratic Quality", "value": "Democratic Quality"},
                {"label": "Delivery Quality", "value": "Delivery Quality"},
                {"label": "Gapminder Life Expectancy",
                    "value": "Gapminder Life Expectancy"},
            ],
            value='Life Ladder',
            clearable=False
        ),

        dcc.Dropdown(
            id="ydropdown",
            options=[
                {"label": "Life Ladder", "value": "Life Ladder"},
                {"label": "Log GDP per capita", "value": "Log GDP per capita"},
                {"label": "Social support", "value": "Social support"},
                {"label": "Healthy life expectancy at birth",
                    "value": "Healthy life expectancy at birth"},
                {"label": "Freedom to make life choices",
                    "value": "Freedom to make life choices"},
                {"label": "Generosity", "value": "Generosity"},
                {"label": "Perceptions of corruption",
                    "value": "Perceptions of corruption"},
                {"label": "Positive affect", "value": "Positive affect"},
                {"label": "Negative affect", "value": "Negative affect"},
                {"label": "Confidence in national government",
                    "value": "Confidence in national government"},
                {"label": "Democratic Quality", "value": "Democratic Quality"},
                {"label": "Delivery Quality", "value": "Delivery Quality"},
                {"label": "Gapminder Life Expectancy",
                    "value": "Gapminder Life Expectancy"},
            ],
            value='Log GDP per capita',
            clearable=False
        ),

        dcc.Graph(
            id='bubblechart'
        ),

        dcc.Slider(
            id='year_slider_bubble',
            min=2007,
            max=2018,
            marks={i: 'Year {}'.format(i) if i == 1 else str(i)
                   for i in range(2007, 2019)},
            value=2007,
        ),

        html.Br(),

        html.Div(
            style={
                'background':'grey'
            },
            children=[html.Br(), html.Br(), html.Br()]
        ),

        html.Br(),

    ])
])


@app.callback(
    Output('mapchart', 'figure'),
    Input('year_slider', 'value'))
def update_figure(selected_year):

    fig = px.choropleth(df, locations="country", locationmode="country names", hover_name="country", color=str(
        selected_year), title="Choropleth", fitbounds="locations")

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
    fig = px.line(d2f[mask], x="Year", y=dropdown,
                  color="Country name", title="Linechart")

    fig.update_layout(
        plot_bgcolor=colors['plotcolor'],
        paper_bgcolor=colors['section'],
        font_color=colors['text'],
    )

    return fig


@app.callback(
    Output('bubblechart', 'figure'),
    Input('year_slider_bubble', 'value'),
    Input('ydropdown', 'value'),
    Input('xdropdown', 'value')
)
def update_figure(year_slider_bubble, xdropdown, ydropdown):
    fig = px.scatter(d2f.query("Year==" + str(year_slider_bubble)), x=xdropdown, y=ydropdown,
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
