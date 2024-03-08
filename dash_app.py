from dash import Dash, html, dcc, callback, Output, Input, dash_table
import pandas as pd
import plotly.express as px

# Define the Dash app creation function
def create_dash_app(flask_app):
    dash_app = Dash(__name__, server=flask_app, url_base_pathname='/dashboard/')
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

    @callback(
        Output('graph-content', 'figure'),
        [Input('dropdown-selection', 'value')]
    )
    def update_graph(value):
        dff = df[df.country==value]
        return px.line(dff, x='year', y='pop')

    dash_app.layout = html.Div([
        html.H1(children='Dash App within Flask', style={'textAlign': 'center'}),
        dcc.Dropdown(options=[{'label': country, 'value': country} for country in df.country.unique()], value='Canada', id='dropdown-selection'),
        dcc.Graph(id='graph-content')
    ])

    return dash_app

def hello_world_dash(flask_app):
    dash_app = Dash(__name__, server=flask_app, url_base_pathname='/hello_word/')
    new_df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

    dash_app.layout = html.Div([
        html.Div(children='Dash Table Data'),
        dash_table.DataTable(data=new_df.to_dict("records"),page_size=10)
    ])
