import dash
from dash import dcc, html, callback_context
from dash.dependencies import Input, Output, State
from app import app
from pages import page1, page2, page3

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Button('Previous Page', id='prev-page-btn', className='nav-button prev-button'),
        html.Button('Next Page', id='next-page-btn', className='nav-button next-button'),
    ], className='navigation'),
    html.Div(id='page-content')
])
@app.callback(Output('url', 'pathname'),
              [Input('prev-page-btn', 'n_clicks'), Input('next-page-btn', 'n_clicks')],
              [State('url', 'pathname')])
def update_url(prev_n_clicks, next_n_clicks, pathname):
    current_page = pathname.strip("/page-")
    current_page = 1 if not current_page.isdigit() else int(current_page)
    max_page = 3

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'prev-page-btn' in changed_id and current_page > 1:
        return f'/page-{current_page - 1}'
    elif 'next-page-btn' in changed_id and current_page < max_page:
        return f'/page-{current_page + 1}'
    return pathname

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/page-1' or pathname == '/':
        return page1.layout()
    elif pathname == '/page-2':
        return page2.layout()
    elif pathname == '/page-3':
        return page3.layout()
    return "404 Page Error"

if __name__ == '__main__':
    app.run_server(debug=True)
