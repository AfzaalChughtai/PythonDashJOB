import dash
from dash import html, dcc
import plotly.graph_objs as go
from data import df, accumulated_sales, profit_ratio, total_discount, average_quantity, average_days_to_ship, total_returns

def layout():
    
    traces = [
        go.Scatter(
            x=df['Order Date'],
            y=df['Sales'],
            mode='lines',
            name='Accumulated Sales',
            line=dict(color='blue')  
        ),
        go.Scatter(
            x=df['Order Date'],
            y=df['Profit'] / df['Sales'], 
            mode='lines',
            name='Profit Ratio',
            line=dict(color='green')  
        ),
        go.Scatter(
            x=df['Order Date'],
            y=df['Discount'],
            mode='lines',
            name='Total Discount',
            line=dict(color='red')  
        ),
        go.Scatter(
            x=df['Order Date'],
            y=df['Quantity'],
            mode='lines',
            name='Average Quantity',
            line=dict(color='orange')  
        ),
        go.Scatter(
            x=df['Order Date'],
            y=df['Ship Date'],
            mode='lines',
            name='Average Days to Ship',
            line=dict(color='purple')  
        ),
        # go.Scatter(
        #     x=df['Order Date'],
        #     y=df['Returned'],
        #     mode='lines',
        #     name='Total Returns',
        #     line=dict(color='brown')  
        # )
    ]

    
    timeline_graph = dcc.Graph(
        id='timeline-graph',
        figure={
            'data': traces,
            'layout': {
                'title': 'Timeline Graph',
                'xaxis': {'title': 'Date'},
                'yaxis': {'title': 'Value'}
            }
        }
    )

    # Date Picker Range
    date_picker_range = dcc.DatePickerRange(
        id='date-picker-range',
        start_date=df['Order Date'].min(),
        end_date=df['Order Date'].max(),
        display_format='YYYY-MM-DD'
    )

   
    granularity_dropdown = dcc.Dropdown(
        id='granularity-dropdown',
        options=[
            {'label': 'Week', 'value': 'W'},
            {'label': 'Month', 'value': 'M'},
            {'label': 'Quarter', 'value': 'Q'},
            {'label': 'Year', 'value': 'Y'}
        ],
        value='M', 
        clearable=False
    )

    return html.Div([
        html.H1('Page 3'),
        html.Div([
            html.P('This is content of Page 3')
        ]),
        
        html.Div([
            html.Label('Date Filter:'),
            date_picker_range,
            html.Label('Granularity:'),
            granularity_dropdown
        ], style={'margin-bottom': '20px'}),
        
        html.Div([
            timeline_graph
        ], style={'width': '50%', 'display': 'inline-block'})
    ])