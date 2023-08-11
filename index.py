from dash import dcc, html, Input, Output
from app import app
from pages import pg1, pg2, pg3

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Home | ', href='/'),
        dcc.Link('pg1 | ', href='/pages/pg1'),
        dcc.Link('pg2 | ', href='/pages/pg2'),
        dcc.Link('pg3 | ', href='/pages/pg3'),

    ], className="row"),
    html.Div(id='page-content', children=[])
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/pg1':
        return pg1.layout
    if pathname == '/pages/pg2':
        return pg2.layout
    if pathname == '/pages/pg3':
        return pg3.layout
    if pathname == '/':
        return "Please choose a link"

if __name__ == '__main__':
    app.run_server(debug=False)
