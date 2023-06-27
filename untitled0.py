import dash
from dash import html as html
from dash import dcc as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


#getting the dataset

data1 = pd.read_csv('https://raw.githubusercontent.com/PhamHuyHoang123/H_H/main/Copy-of-adidas.csv')

#dash app

app = dash.Dash(__name__)

#layout
app.layout = html.Div(children = [
    html.Div([
        html.H1(children = 'Financial Analysis of Adidas'
                )
    ]),
    html.Div([
        html.Div([
            dcc.Dropdown(
                id = 'geo-dropdown',
                options = [{'label': i, 'value': i}
                           for i in data1['Product'].unique()],
                value = "Men's Street Footwear"
            ),
            dcc.Graph(id = 'price-graph')
        ], className='six columns'),
        html.Div([
            dcc.Graph(id = 'bar-chart')
        ], className='six columns')
    ], className='row'),
    html.Div([
        html.Div([
            html.Label('Select a category:'),
            dcc.Dropdown(
                id = 'my_dropdown',
                options = [{'label': 'Retailers', 'value': 'Retailer'},
                           {'label': 'Sales Method', 'value': 'Sales Method'}
                          ],
                value = 'Retailer',
                multi = False,
                clearable = False,
            ),
            dcc.Graph(id = 'the_graph')
        ])
    ], className='row')
])

@app.callback(
    Output(component_id = 'price-graph', component_property ='figure'),
    Input(component_id = 'geo-dropdown', component_property = 'value')
)
def update_scatter(selected_product):
    a = data1[data1['Product'] == selected_product]
    graph = px.scatter(a, x ='Units Sold', y = 'Operating Profit', color = 'Sales Method')
    return graph

@app.callback(
    Output(component_id = 'bar-chart', component_property ='figure'),
    Input(component_id = 'geo-dropdown', component_property = 'value')
)
def update_bar(selected_product):
    b = data1[data1['Product'] == selected_product]
    bar = px.histogram(b, x ='Sales Method', histfunc='count')
    return bar


@app.callback(
    Output(component_id = 'the_graph', component_property = 'figure'),
    Input(component_id = 'my_dropdown', component_property = 'value')
)
def update_pie(selected_column):
    if selected_column == 'Retailer':
        piechart = px.pie(data_frame = data1, names = 'Retailer', hole = 0.3)
    elif selected_column == 'Sales Method':
        piechart = px.pie(data_frame = data1, names = 'Sales Method', hole = 0.3)
    return piechart

if __name__ == '__main__':
    app.run_server(debug = True)
