import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, State
import sys
import os

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import config

# Initialize Dash application
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
    ],
    suppress_callback_exceptions=True,
    assets_folder='assets'
)
app.title = "VoteVision AI - Election Command Center"
server = app.server

# Import page modules
from dashboard.pages import home, analytics, prediction, risk, simulator, planner, admin, about

# Accessibility bar layout
accessibility_bar = html.Div([
    html.Div([
        html.I(className="fa-solid fa-language me-1", style={'color': '#60A5FA'}),
        dcc.Dropdown(
            id='lang-selector',
            options=[
                {'label': 'English', 'value': 'en'},
                {'label': 'हिन्दी (Hindi)', 'value': 'hi'},
                {'label': 'ಕನ್ನಡ (Kannada)', 'value': 'kn'}
            ],
            value='en',
            clearable=False,
            className="lang-selector d-inline-block",
            style={'width': '120px'}
        )
    ], className="d-flex align-items-center me-3"),
    
    html.Div([
        html.I(className="fa-solid fa-circle-half-stroke me-1", style={'color': '#FACC15'}),
        dbc.Button("Contrast Toggle", id="contrast-toggle-btn", color="link", size="sm", className="p-0 text-decoration-none", style={'color': '#94A3B8', 'fontSize': '0.8rem'}),
    ], className="d-flex align-items-center me-3"),
    
    html.Div([
        html.Span("● LIVE FEED ACTIVE", className="badge bg-success active-pulse", style={'fontSize': '0.7rem'})
    ], className="d-flex align-items-center")
], className="accessibility-bar")

# Master layout with location and state store
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='lang-store', data='en'),
    dcc.Store(id='contrast-store', data='normal'),
    
    dbc.Container([
        dbc.Row([
            # Collapsible Sidebar Column
            dbc.Col([
                html.Div([
                    # Sidebar Title Header & Hamburger Button
                    html.Div([
                        html.Div(id='sidebar-title-container', className="flex-grow-1"),
                        
                        # Mobile menu hamburger toggler
                        dbc.Button(
                            html.I(className="fa-solid fa-bars"), 
                            id="sidebar-toggler", 
                            color="link", 
                            className="d-block d-md-none text-white p-0 fs-4",
                            style={"outline": "none", "boxShadow": "none", "textDecoration": "none"}
                        )
                    ], className="d-flex align-items-center justify-content-between w-100"),
                    
                    # Collapsible Nav links
                    dbc.Collapse(
                        html.Div([
                            html.Hr(style={'borderColor': '#1E293B'}),
                            html.Div(id='sidebar-nav-container'),
                            html.Div([
                                html.Hr(style={'borderColor': '#1E293B'}),
                                html.Div("v1.0.0 (Command Room)", style={'fontSize': '0.7rem', 'color': '#64748B', 'textAlign': 'center', 'marginBottom': '0.3rem'}),
                                html.Div("© 2026 VoteVision AI.", style={'fontSize': '0.65rem', 'color': '#64748B', 'textAlign': 'center'}),
                                html.Div("All Rights Reserved to Developer.", style={'fontSize': '0.65rem', 'color': '#64748B', 'textAlign': 'center'})
                            ], className="mt-auto px-2 pt-4")
                        ], className="d-flex flex-column h-100 w-100"),
                        id="sidebar-collapse",
                        is_open=False,
                        className="d-md-block w-100"
                    )
                ], className="sidebar")
            ], id='sidebar-column', width=12, md=3, lg=2, style={'padding': '0', 'zIndex': '100'}),
            
            # Content column
            dbc.Col([
                accessibility_bar,
                html.Div(id='page-content', style={'padding': '2rem', 'minHeight': 'calc(100vh - 40px)'})
            ], width=12, md=9, lg=10, style={'padding': '0', 'backgroundColor': '#0B1220'})
        ], className="g-0")
    ], fluid=True)
], id="master-container")

# Callback to persist and sync language selection
@app.callback(
    Output('lang-store', 'data'),
    Input('lang-selector', 'value')
)
def sync_language(lang_val):
    return lang_val

# Callback to toggle high contrast mode styling
@app.callback(
    Output('contrast-store', 'data'),
    Output('master-container', 'style'),
    Input('contrast-toggle-btn', 'n_clicks'),
    State('contrast-store', 'data'),
    prevent_initial_call=True
)
def toggle_contrast(n_clicks, current_mode):
    if current_mode == 'normal':
        new_mode = 'contrast'
        style = {
            'filter': 'contrast(1.2) saturate(1.1)',
            'backgroundColor': '#000000'
        }
    else:
        new_mode = 'normal'
        style = {}
    return new_mode, style

# Callback to update sidebar contents based on active language selection
@app.callback(
    Output('sidebar-title-container', 'children'),
    Output('sidebar-nav-container', 'children'),
    Input('lang-store', 'data')
)
def update_sidebar_contents(lang):
    texts = config.LANGUAGES.get(lang, config.LANGUAGES['en'])
    
    title_section = html.Div([
        html.Div(texts['title'], className="sidebar-title"),
        html.Div(texts['subtitle'], className="sidebar-subtitle"),
    ], className="px-2")
    
    nav_section = dbc.Nav([
        dbc.NavLink([html.I(className="fa-solid fa-gauge me-2"), texts['command_center']], href="/", active="exact", id="nav-home"),
        dbc.NavLink([html.I(className="fa-solid fa-chart-line me-2"), texts['live_turnout']], href="/analytics", active="exact", id="nav-analytics"),
        dbc.NavLink([html.I(className="fa-solid fa-brain me-2"), texts['prediction_center']], href="/prediction", active="exact", id="nav-prediction"),
        dbc.NavLink([html.I(className="fa-solid fa-triangle-exclamation me-2"), texts['risk_intel']], href="/risk", active="exact", id="nav-risk"),
        dbc.NavLink([html.I(className="fa-solid fa-sliders me-2"), texts['what_if']], href="/simulator", active="exact", id="nav-simulator"),
        dbc.NavLink([html.I(className="fa-solid fa-bullhorn me-2"), texts['recommendations']], href="/planner", active="exact", id="nav-planner"),
        dbc.NavLink([html.I(className="fa-solid fa-gears me-2"), texts['admin_panel']], href="/admin", active="exact", id="nav-admin"),
        dbc.NavLink([html.I(className="fa-solid fa-circle-info me-2"), texts['about']], href="/about", active="exact", id="nav-about"),
    ], vertical=True, pills=True, className="flex-column flex-nowrap")
    
    return title_section, nav_section

# Unified Callback to handle sidebar collapsing/expanding state
from dash import ctx
@app.callback(
    Output("sidebar-collapse", "is_open"),
    Input("sidebar-toggler", "n_clicks"),
    Input("url", "pathname"),
    State("sidebar-collapse", "is_open"),
    prevent_initial_call=True
)
def handle_sidebar_collapse(n_clicks, pathname, is_open):
    triggered_id = ctx.triggered_id
    if triggered_id == "sidebar-toggler":
        return not is_open
    elif triggered_id == "url":
        return False
    return is_open


# Main Routing Callback
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
    Input('lang-store', 'data')
)
def render_page_content(pathname, lang):
    if pathname == '/':
        return home.get_layout(lang=lang)
    elif pathname == '/analytics':
        return analytics.get_layout(lang=lang)
    elif pathname == '/prediction':
        return prediction.get_layout(lang=lang)
    elif pathname == '/risk':
        return risk.get_layout(lang=lang)
    elif pathname == '/simulator':
        return simulator.get_layout(lang=lang)
    elif pathname == '/planner':
        return planner.get_layout(lang=lang)
    elif pathname == '/admin':
        return admin.get_layout(lang=lang)
    elif pathname == '/about':
        return about.get_layout(lang=lang)
    else:
        return html.Div([
            html.H1("404: Page Not Found", style={'color': '#EF4444'}),
            html.P(f"Path '{pathname}' was not recognized by the command system."),
            dbc.Button("Return to Command Center", href="/", color="primary")
        ], className="text-center py-5")

if __name__ == '__main__':
    # We run on 8050 as standard for local testing and disable the DevTools UI panel
    app.run(debug=True, port=8050, dev_tools_ui=False)
