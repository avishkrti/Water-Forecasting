import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pages import page1

# import flask

# server = flask.Flask(__name__, template_folder='assets')
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 0.7rem",
    "background-color": "#2d3154",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.Link(rel='stylesheet', href='https://raw.githubusercontent.com/avishkrti/Water-Forecasting/main/assets/custom.css'),
        html.H1("Water Management", style={"color": "white",}),
        html.Hr(),
        html.P(
            "Select the Reservoir", className="lead", style={"color": "white","font-weight":"bold"}
        ),
        dbc.Nav(
            [
                dbc.NavLink("KRS", href="/pages/page1", active="exact",  style={"color": "white","font-weight":"bold"}),
                dbc.NavLink("HARANGI", href="/page-2", active="exact", style={"color": "white","font-weight":"bold"}),
                dbc.NavLink("HEMATI", href="/page-3", active="exact", style={"color": "white","font-weight":"bold"}),
                dbc.NavLink("KABINI", href="/page-4", active="exact", style={"color": "white","font-weight":"bold"}),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/pages/page1":
        return page1.layout()
    elif pathname == "/page-2":
        return html.P("Under Construction!")
    elif pathname == "/page-3":
        return html.P("Under Construction!")
    elif pathname == "/page-4":
        return html.P("Under Construction!")
    else:
        return page1.layout()
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

@ app.server.route('/dynamic/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'dynamic')
    return send_from_directory(dynamic, path)


if __name__ == "__main__":
    app.run_server(port=8050, debug=False)