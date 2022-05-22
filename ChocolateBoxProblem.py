'''
If one was to drop a box of N chocolates and place them all back randomly, 
the probability that all of the chocolates went into a different spot than 
their original spot is 1/e as N goes to infinity. Let's model this!
'''
from math import e
import random
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np


app = Dash(__name__)

colors = {
    'background': '#111111',
    'text': '#FFFFFF',
    'level1': '#181818',
    'level2': '#404040',
}

#Returns true if none of the chocolates went into the correct position
def check(l1, l2):
    for num1, num2 in zip(l1, l2):
        if num1 == num2:
            return False
    return True

def create_data(num_chocolates, num_iter):
    #The box of chocolates is represented by a random list of numbers, each defining a unique position in the box
    original_pos = random.sample(range(1, num_chocolates+1), num_chocolates)
    #columns for pandas dataframe
    ratio = []
    num_different = 0
    for i in range(1, num_iter+1):
        new_pos = random.sample(range(1, num_chocolates+1), num_chocolates)
        if check(original_pos, new_pos):
            num_different += 1
        ratio.append(num_different / i)
    data = pd.DataFrame({'iterations': np.arange(1, num_iter+1), 'ratio': ratio, '1/e': 1/e})
    return data

#Create Data with dummy values
data = create_data(100, 100)
fig = px.line(data, x='iterations', y=data.columns[1:])

#Display in app
app.layout = html.Div(
    style={
        'backgroundColor': colors['background']
    },
    children=[
    html.H1(
        children='The Chocolate Box Problem',
        style={
            'textAlign': 'left',
            'color': colors['text'],
        }
    ),
    html.Div(children=
            '''
            Suppose I have a box of chocolates having 100 chocolates,
            and I drop them all on the ground, and then I try to put them all back in. 
            What is the probability that every chocolate went back in a wrong spot?
            ''', 
            style={
                'textAlign': 'center',
                'color': colors['text']}
    ),
    html.Br(),
    html.Br(),
    html.Div(id='data',style={
        'backgroundColor': colors['level1'],
        'padding': 10
    },
        children=[
        html.Div(id="graph", children=[
            dcc.Graph(
                id='probability-graph',
                figure=fig,
                style={
                    'plot_bgcolor': colors['level1'],
                    'backgroundColor': colors['level1'],
                    'color': colors['text'],
                    'padding': 10, 
                }
            ),
        ]),
        html.Div(
            style={
                'backgroundColor': colors['level2'],
                'padding': 10, 
            },
            children=[
            html.Div(children=
                '''
                The red line represents y = 1/e. The blue line represents the current probability of every chocolate not going back to its original position.
                This is done through simulating N chocolates for M iterations. Play around with the sliders to adjust the number of chocolates and iterations,
                and see how close to 1/e you can get!
                ''', 
                style={
                    'textAlign': 'center',
                    'color': colors['text']}
            ),
            html.H1(
            children='Pick number of chocolates',
            style={
                'textAlign': 'center',
                'color': colors['text']
            }
            ),
            dcc.Slider(
                    id='chocolates-slider',
                    min=1,
                    max=1000,
                    marks={i: str(i) for i in range(0, 1001, 100)},
                    value=5,
            ),
            html.H1(
                children='Pick maximum number of iterations',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }
            ),
            dcc.Slider(
                    id='iter-slider',
                    min=1,
                    max=1000,
                    marks={i: str(i) for i in range(0, 1001, 100)},
                    value=5,
            )
        ])
    ])
])

# Callbacks
@app.callback(
    Output('probability-graph', 'figure'),
    Input('chocolates-slider', 'value'),
    Input('iter-slider', 'value'))
def update_iterations(num_chocolates, num_iter):
    new_data = create_data(num_chocolates, num_iter)
    fig = px.line(new_data, x='iterations', y=data.columns[1:])
    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)