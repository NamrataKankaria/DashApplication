# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

app = dash.Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Cucumber", "Apples", "Oranges", "Bananas", "Cucumber"],
    "Amount": [4, 1, 2, 2, 4, 5, 1, 2],
    "City": ["SF", "SF", "SF", "SF", "Montreal", "Montreal", "Montreal", "Montreal"]
})
df_scatter = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/'
                         'a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

df_callback = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
fig_scatter = px.scatter(df_scatter, x="gdp per capita", y="life expectancy", size="population", color="continent",
                         hover_name="country", log_x=True, size_max=60)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),

    dcc.Graph(
        id='example-scatter',
        figure=fig_scatter
    ),
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=df_callback['year'].min(),
        max=df_callback['year'].max(),
        value=df_callback['year'].min(),
        marks={str(year): str(year) for year in df_callback['year'].unique()},
        step=None),

    html.Div([
        html.H1(children='Callback Test', id='h1_callback'),
        html.Button(id='btn_callback', children='Button Name', n_clicks=0)
    ])
])


@app.callback(
    Output('h1_callback', 'children'),
    Input('btn_callback', 'n_clicks')
)
def update_button(btn_click):
    return u'Input 1 is "{}"'.format(btn_click)


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    filtered_df = df_callback[df_callback.year == selected_year]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
