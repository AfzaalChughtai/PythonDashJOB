
from dash import html, dcc
from data import df, accumulated_sales, profit_ratio, total_discount, average_quantity

import plotly.express as px

df_sorted = df.sort_values(by=['Category', 'Sales'], ascending=[True, False])

df_top5 = df_sorted.groupby('Category').head(5)

figg = px.bar(df_top5, x='Sales', y='Category', title='Top 5 Sales by Category', orientation='h')

figg.update_layout(
    yaxis_title='Category',
    xaxis_title='Sales',
    yaxis={'categoryorder':'total ascending'},  
    xaxis=dict(type='linear'),
    bargap=0.2,
)

figg.update_traces(texttemplate='%{x}', textposition='outside')



df['Month_Year'] = df['Order Date'].dt.to_period('M').astype(str)

monthly_sales = df.groupby('Month_Year')['Sales'].sum().reset_index()

fig = px.bar(monthly_sales, x='Month_Year', y='Sales', title='Monthly Sales')


fig.update_layout(
    xaxis_title='Month-Year',
    yaxis_title='Sales',
    xaxis=dict(tickangle=-45),  
    bargap=0.2,  
)


fig.update_traces(texttemplate='%{y}', textposition='outside')













def layout():
    return html.Div([
        html.H1('Dashboard Overview'),
        dcc.Graph(figure=figg),
        dcc.Graph(figure=fig),
        html.Div([
            html.H3(f'Accumulated Sales: {accumulated_sales:,.2f}'),
            html.H3(f'Profit Ratio: {profit_ratio:.2%}'),
            html.H3(f'Total Discount: {total_discount:,.2f}'),
            html.H3(f'Average Quantity: {average_quantity:.2%}')
        ]),
       
        html.Div([
            html.Div(dcc.Link('Go to Page 2', href='/page-2'), className='nav-card'),
            html.Div(dcc.Link('Go to Page 3', href='/page-3'), className='nav-card'),
        ], className='card-container')
    ])
