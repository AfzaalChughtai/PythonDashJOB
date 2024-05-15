import dash
from dash import html, dcc, dash_table, callback
from dash.dependencies import Input, Output, State
from data import df


def layout():
    country_options = [{'label': country, 'value': country} for country in sorted(df['Country'].unique())]
    
    return html.Div([
        html.H1('Page 2'),
        dcc.Dropdown(id='country-dropdown', options=country_options, placeholder='Select Country'),
        dcc.Dropdown(id='state-dropdown', placeholder='Select State', disabled=True),
        dcc.Dropdown(id='city-dropdown', placeholder='Select City', disabled=True),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            filter_action='native',  
            style_table={'height': '300px', 'overflowY': 'auto', 'width': '100%'},  
        ),
        html.Div([
            html.Div([
                dcc.Input(id='input-1', type='text', placeholder='Order ID'),
                dcc.Input(id='input-2', type='text', placeholder='Order Date'),
                dcc.Input(id='input-3', type='text', placeholder='Ship Date'),
                dcc.Input(id='input-4', type='text', placeholder='Ship Mode'),
                dcc.Input(id='input-5', type='text', placeholder='Customer ID'),
                html.Button('Add', id='add-button', n_clicks=0)
            ])
        ])
    ])
@callback(
    [Output('state-dropdown', 'options'),
     Output('state-dropdown', 'disabled'),
     Output('city-dropdown', 'options'),
     Output('city-dropdown', 'disabled')],
    [Input('country-dropdown', 'value'),
     Input('state-dropdown', 'value')],
    prevent_initial_call=True  
)
def set_state_and_city_options(selected_country, selected_state):
    ctx = dash.callback_context
    if not ctx.triggered:
        
        return [], True, [], True
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger_id == 'country-dropdown':
            states = df[df['Country'] == selected_country]['State'].unique() if selected_country else []
            return [{'label': state, 'value': state} for state in states], not selected_country, [], True
        elif trigger_id == 'state-dropdown':
            cities = df[(df['Country'] == selected_country) & (df['State'] == selected_state)]['City'].unique() if selected_state else []
            return dash.no_update, dash.no_update, [{'label': city, 'value': city} for city in cities], not selected_state
        return [], True, [], True

@callback(
    [Output('table', 'data')],
    [Input('country-dropdown', 'value'),
     Input('state-dropdown', 'value'),
     Input('city-dropdown', 'value'),
     Input('add-button', 'n_clicks')],
    [State('table', 'data'),
     State('input-1', 'value'),
     State('input-2', 'value'),
     State('input-3', 'value'),
     State('input-4', 'value'),
     State('input-5', 'value')]
)
 
def update_table(selected_country, selected_state, selected_city, n_clicks, current_data, input1, input2, input3, input4, input5):
    ctx = dash.callback_context
    if not ctx.triggered:
        return [current_data]
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger_id == 'add-button':
            new_entry = {
                'Order ID': input1,
                'Order Date': input2,
                'Ship Date': input3,
                'Ship Mode': input4,
                'Customer ID': input5,
                'Row ID': len(current_data) + 1 
            }
            updated_data = current_data + [new_entry]
            return [updated_data]
        else:
            filtered_df = df
            if selected_country:
                filtered_df = filtered_df[filtered_df['Country'] == selected_country]
            if selected_state:
                filtered_df = filtered_df[filtered_df['State'] == selected_state]
            if selected_city:
                filtered_df = filtered_df[filtered_df['City'] == selected_city]
            return [filtered_df.to_dict('records')]