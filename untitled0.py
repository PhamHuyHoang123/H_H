import dash
from dash import html as html
from dash import dcc as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

#getting the dataset
pro = pd.read_csv('C:/Users/huyho/Documents/code/data/Coffee_Chain.csv')

# remove commas from 'Budget_sales' column and convert to integers
pro['Budget_sales'] = pro['Budget_sales'].str.replace(',', '').astype(int)

#dash app
app = dash.Dash(__name__)
server = app.server

#layout
app.layout = html.Div(children = [
    html.H1('Introduction'),
    html.P('Python is a versatile and powerful programming language that is widely used for developing various types of applications. It has gained immense popularity due to its simplicity, readability, and vast collection of libraries and frameworks.'),
    html.P('Python can be used for developing a wide range of applications, including web applications, desktop applications, scientific and numeric computing, machine learning and artificial intelligence, data analysis and visualization, automation and scripting, and more. With Python, developers can leverage its rich ecosystem of packages to quickly implement complex functionalities and create user-friendly interfaces.'),
    html.P('Whether it\'s a web app, desktop app, or command-line tool, Python provides the flexibility and versatility needed to build powerful applications.'),
    html.Div([
        html.H1(children = 'Coffee Chain Dashboard',
                style={'text-align': 'center', 'font-size': '36px', 'color': '#333333', 'margin': '10px'})
    ]),
    html.Div([
        html.Div([
            html.Label('Select types of product:', style={'color': '#1F618D'}),
            dcc.Checklist(
                id='geo-checklist',
                options=[{'label': i, 'value': i} for i in pro['Product_type'].unique()],
                value=['Coffee'],
                labelStyle={'display': 'block', 'margin': '10px'}
            ),
            dcc.Dropdown(
                id='state-dropdown',
                options=[{'label': i, 'value': i} for i in pro['State'].unique()],
                value=[],
                multi=True,
                placeholder='Select many states that you want to be shown'
            ),
            dcc.Graph(id='price-graph'),
        ], className='six columns', style={'border': '1px solid #ced4da', 'border-radius': '5px', 'margin': '10px'}),
        html.Div([
            dcc.Graph(id='scatter-chart'),
            html.Div([
                html.Label('Range of budget sales:', style={'color': '#1F618D'}),
                dcc.RangeSlider(
                    id='range-slider',
                    min=pro['Budget_sales'].min(),
                    max=pro['Budget_sales'].max(),
                    step=1,
                    value=[pro['Budget_sales'].min(), pro['Budget_sales'].max()],
                    marks={i: str(i) for i in range(pro['Budget_sales'].min(), pro['Budget_sales'].max()+1, 100)}
                )
            ], style={'margin': '20px'})
        ], className='six columns', style={'border': '1px solid #ced4da', 'border-radius': '5px', 'margin': '10px'})
    ], className='row')
])

@app.callback(
    Output(component_id='price-graph', component_property='figure'),
    Input(component_id='geo-checklist', component_property='value'),
    Input(component_id='state-dropdown', component_property='value')
)
def update_bar(selected_departments, selected_states):
    data = pro[pro['Product_type'].isin(selected_departments)]
    if selected_states:
        data = data[data['State'].isin(selected_states)]
    bar = px.histogram(data, x='State', nbins=30, color_discrete_sequence=['green'])
    bar.update_layout(
        plot_bgcolor='#f8f8f8', paper_bgcolor='#f8f8f8',
        font_color='#333333', title_font_size=30,
        xaxis_title='State', yaxis_title='Count'
    )
    return bar

@app.callback(
    Output(component_id='scatter-chart', component_property='figure'),
    Input(component_id='geo-checklist', component_property='value'),
    Input(component_id='state-dropdown', component_property='value'),
    Input(component_id='range-slider', component_property='value')
)
def update_scatter(selected_departments, selected_states, selected_range):
    data = pro[pro['Product_type'].isin(selected_departments) & (pro['Budget_sales'] >= selected_range[0]) & (pro['Budget_sales'] <= selected_range[1])]
    if selected_states:
        data = data[data['State'].isin(selected_states)]
    graph = px.scatter(data, x='Budget_sales', y='Budget_profit', color='Product')
    graph.update_layout(
        plot_bgcolor='#f8f8f8', paper_bgcolor='#f8f8f8',
        font_color='#333333', title_font_size=30,
        xaxis_title='Budget sales', yaxis_title='Budget profit'
    )
    return graph

if __name__ == '__main__':
    app.run_server(debug=True)
