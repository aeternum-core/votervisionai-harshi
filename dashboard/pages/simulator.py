from dash import html, dcc, callback, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import sys
import os

# Ensure parent directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import config
from services.data_service import DataService

data_service = DataService()

def get_layout(lang='en'):
    states = data_service.get_states()
    state_options = [{'label': s, 'value': s} for s in states]
    
    # Preset Selector Section
    selector_card = dbc.Card([
        dbc.Row([
            dbc.Col([
                html.Label("Select State", className="form-label-custom"),
                dcc.Dropdown(
                    id='sim-state-select',
                    options=state_options,
                    value=states[0] if states else None,
                    clearable=False,
                    className="bg-dark text-white border-secondary"
                )
            ], md=4),
            dbc.Col([
                html.Label("Select District", className="form-label-custom"),
                dcc.Dropdown(
                    id='sim-district-select',
                    options=[],
                    clearable=False,
                    className="bg-dark text-white border-secondary"
                )
            ], md=4),
            dbc.Col([
                html.Label("Select Constituency Cell", className="form-label-custom"),
                dcc.Dropdown(
                    id='sim-constituency-select',
                    options=[],
                    clearable=False,
                    className="bg-dark text-white border-secondary"
                )
            ], md=4),
        ], className="g-3")
    ], className="stat-card mb-4 overflow-visible", style={'padding': '1.2rem'})

    # Prebuilt Scenario Library Card
    scenario_library = dbc.Card([
        html.H6("Election Scenario Library™", className="mb-3", style={'fontFamily': 'Poppins', 'color': '#F8FAFC', 'fontSize': '0.9rem'}),
        html.Div([
            dbc.Button("🌧️ Torrential Rain / Extreme Heat", id='preset-rain', color="danger", size="sm", className="me-2 mb-2", style={'fontSize': '0.75rem', 'fontWeight': '500'}),
            dbc.Button("📢 Intense Awareness Drive", id='preset-campaign-boost', color="success", size="sm", className="me-2 mb-2", style={'fontSize': '0.75rem', 'fontWeight': '500'}),
            dbc.Button("📅 Holiday Drag Effect", id='preset-holiday-drag', color="warning", size="sm", className="me-2 mb-2", style={'fontSize': '0.75rem', 'fontWeight': '500'}),
            dbc.Button("🚀 Midweek Transit Mobilization", id='preset-midweek', color="info", size="sm", className="me-2 mb-2", style={'fontSize': '0.75rem', 'fontWeight': '500'})
        ], className="d-flex flex-wrap")
    ], className="stat-card p-3 mb-3")

    # Sliders Card
    sliders_card = dbc.Card([
        html.H5("Simulate Operational Adjustments", className="mb-4", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
        
        html.Div([
            html.Label("Awareness Campaign Boost (0% to +30%)", className="form-label-custom"),
            dcc.Slider(0, 30, 1, value=0, id='sim-boost-awareness', 
                       marks={0: '0', 10: '+10%', 20: '+20%', 30: '+30%'}, className="mb-4")
        ]),
        
        html.Div([
            html.Label("Transport Shuttle Access Improvement (0% to +30%)", className="form-label-custom"),
            dcc.Slider(0, 30, 1, value=0, id='sim-boost-transport', 
                       marks={0: '0', 10: '+10%', 20: '+20%', 30: '+30%'}, className="mb-4")
        ]),
        
        html.Div([
            html.Label("Weather Severity Adjustment (Rain/Heat) (-30% to +10%)", className="form-label-custom"),
            dcc.Slider(-30, 10, 1, value=0, id='sim-adjust-weather', 
                       marks={-30: 'Extreme', -15: 'Harsh', 0: 'Baseline', 10: 'Pleasant'}, className="mb-4")
        ]),
        
        html.Div([
            html.Label("Holiday Proximity Impact Toggle", className="form-label-custom"),
            dcc.Dropdown(
                id='sim-adjust-holiday',
                options=[
                    {'label': 'No Proximity Weekend (No Change)', 'value': 'keep'},
                    {'label': 'Simulate Near 3-Day Weekend (Apply Holiday Drag)', 'value': 'apply_holiday'},
                    {'label': 'Simulate Isolated Midweek Election (Apply Boost)', 'value': 'remove_holiday'}
                ],
                value='keep',
                clearable=False,
                className="bg-dark text-white border-secondary mb-4"
            )
        ]),
        
        dbc.Button("Reset to Region Baseline", id='sim-reset-btn', color="secondary", className="w-100", style={'fontWeight': '600'})
    ], className="stat-card p-4 overflow-visible")

    # Outputs card
    outputs_panel = html.Div([
        # Comparison Gauges and metrics
        dbc.Card([
            html.H5("Simulation Forecast Delta", className="mb-4", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
            
            dbc.Row([
                dbc.Col([
                    html.Div("Baseline Forecast", style={'fontSize': '0.85rem', 'color': '#94A3B8'}),
                    html.Div(id='sim-out-base-turnout', style={'fontSize': '2rem', 'fontWeight': 'bold', 'color': '#94A3B8'}),
                    html.Div(id='sim-out-base-risk', className="badge bg-secondary", style={'fontSize': '0.75rem'})
                ], md=4, className="text-center mb-3"),
                
                dbc.Col([
                    html.Div("Simulated Forecast", style={'fontSize': '0.85rem', 'color': '#94A3B8'}),
                    html.Div(id='sim-out-new-turnout', style={'fontSize': '2.6rem', 'fontWeight': 'bold', 'color': '#60A5FA'}),
                    html.Div(id='sim-out-new-risk', className="badge bg-primary", style={'fontSize': '0.85rem'})
                ], md=4, className="text-center border-start border-end border-secondary mb-3"),
                
                dbc.Col([
                    html.Div("Estimated Impact", style={'fontSize': '0.85rem', 'color': '#94A3B8'}),
                    html.Div(id='sim-out-delta', style={'fontSize': '2.2rem', 'fontWeight': 'bold', 'color': '#22C55E'}),
                    html.Div("Projected change", style={'fontSize': '0.75rem', 'color': '#94A3B8'})
                ], md=4, className="text-center mb-3")
            ], className="align-items-center mb-3"),
            
            html.Hr(style={'borderColor': '#1E293B'}),
            
            # Sub-indicators
            dbc.Row([
                dbc.Col([
                    html.Div("Awareness Score", style={'fontSize': '0.75rem', 'color': '#94A3B8'}),
                    html.Div(id='sim-out-awareness-val', style={'fontWeight': 'bold', 'color': '#F8FAFC'})
                ], xs=4, className="text-center"),
                dbc.Col([
                    html.Div("Transport Score", style={'fontSize': '0.75rem', 'color': '#94A3B8'}),
                    html.Div(id='sim-out-transport-val', style={'fontWeight': 'bold', 'color': '#F8FAFC'})
                ], xs=4, className="text-center"),
                dbc.Col([
                    html.Div("Weather Score", style={'fontSize': '0.75rem', 'color': '#94A3B8'}),
                    html.Div(id='sim-out-weather-val', style={'fontWeight': 'bold', 'color': '#F8FAFC'})
                ], xs=4, className="text-center")
            ])
        ], className="stat-card mb-4"),
        
        # Plot comparison
        dbc.Card([
            dcc.Graph(id='sim-comparison-plot', config={'displayModeBar': False})
        ], className="stat-card")
    ])

    return html.Div([
        # Title
        html.Div([
            html.H3("What-If Operational Scenario Lab", style={'fontFamily': 'Poppins', 'fontWeight': '600', 'color': '#F8FAFC'}),
            html.P("Simulate variations in weather conditions and test intervention policies to forecast turnout changes.", style={'color': '#94A3B8'})
        ], className="mb-4"),
        
        selector_card,
        
        dbc.Row([
            dbc.Col([scenario_library, sliders_card], lg=6, md=12, className="mb-4"),
            dbc.Col(outputs_panel, lg=6, md=12, className="mb-4")
        ])
    ])

# Callbacks for selectors
@callback(
    Output('sim-district-select', 'options'),
    Output('sim-district-select', 'value'),
    Input('sim-state-select', 'value')
)
def update_sim_districts(selected_state):
    districts = data_service.get_districts(state=selected_state)
    options = [{'label': d, 'value': d} for d in districts]
    val = districts[0] if districts else None
    return options, val

@callback(
    Output('sim-constituency-select', 'options'),
    Output('sim-constituency-select', 'value'),
    Input('sim-district-select', 'value'),
    State('sim-state-select', 'value')
)
def update_sim_constituencies(selected_district, selected_state):
    if not selected_district:
        return [], None
    consts = data_service.get_constituencies(state=selected_state, district=selected_district)
    options = [{'label': c, 'value': c} for c in consts]
    val = consts[0] if consts else None
    return options, val

# Callback to load Prebuilt Scenarios Library
@callback(
    Output('sim-boost-awareness', 'value', allow_duplicate=True),
    Output('sim-boost-transport', 'value', allow_duplicate=True),
    Output('sim-adjust-weather', 'value', allow_duplicate=True),
    Output('sim-adjust-holiday', 'value', allow_duplicate=True),
    Input('preset-rain', 'n_clicks'),
    Input('preset-campaign-boost', 'n_clicks'),
    Input('preset-holiday-drag', 'n_clicks'),
    Input('preset-midweek', 'n_clicks'),
    prevent_initial_call=True
)
def load_scenario_preset(rain, campaign, holiday, midweek):
    trig_id = ctx.triggered_id
    if trig_id == 'preset-rain':
        return 0, 0, -25, 'keep'
    elif trig_id == 'preset-campaign-boost':
        return 20, 10, 0, 'keep'
    elif trig_id == 'preset-holiday-drag':
        return 0, 0, 0, 'apply_holiday'
    elif trig_id == 'preset-midweek':
        return 10, 20, 5, 'remove_holiday'
    return 0, 0, 0, 'keep'

# Callback to reset sliders
@callback(
    Output('sim-boost-awareness', 'value'),
    Output('sim-boost-transport', 'value'),
    Output('sim-adjust-weather', 'value'),
    Output('sim-adjust-holiday', 'value'),
    Input('sim-reset-btn', 'n_clicks'),
    prevent_initial_call=True
)
def reset_simulation_sliders(n_clicks):
    return 0, 0, 0, 'keep'

# Central prediction mapping callback
@callback(
    Output('sim-out-base-turnout', 'children'),
    Output('sim-out-base-risk', 'children'),
    Output('sim-out-base-risk', 'className'),
    Output('sim-out-new-turnout', 'children'),
    Output('sim-out-new-risk', 'children'),
    Output('sim-out-new-risk', 'className'),
    Output('sim-out-delta', 'children'),
    Output('sim-out-delta', 'style'),
    Output('sim-out-awareness-val', 'children'),
    Output('sim-out-transport-val', 'children'),
    Output('sim-out-weather-val', 'children'),
    Output('sim-comparison-plot', 'figure'),
    Input('sim-constituency-select', 'value'),
    Input('sim-boost-awareness', 'value'),
    Input('sim-boost-transport', 'value'),
    Input('sim-adjust-weather', 'value'),
    Input('sim-adjust-holiday', 'value'),
    State('sim-state-select', 'value'),
    State('sim-district-select', 'value')
)
def run_what_if_simulation(constituency, boost_awareness, boost_transport, adjust_weather, adjust_holiday, state, district):
    if not constituency:
        return "N/A", "N/A", "badge bg-secondary", "N/A", "N/A", "badge bg-secondary", "0.00%", {'color': '#94A3B8'}, "N/A", "N/A", "N/A", go.Figure()
        
    df = data_service.df
    row = df[(df['state'] == state) & (df['district'] == district) & (df['constituency'] == constituency)].iloc[0]
    
    # 1. Base values
    base_hist = float(row['historical_turnout'])
    base_lit = float(row['literacy_rate'])
    base_type = str(row['region_type'])
    
    base_aware = int(row['awareness_score'])
    base_trans = int(row['transport_accessibility'])
    base_weather = int(row['weather_score'])
    base_campaign = int(row['campaign_intensity'])
    base_holiday = int(row['holiday_factor'])
    
    # Predict baseline final expected turnout using models
    base_pred_turnout, base_risk_label, _ = data_service.predict_region(
        historical_turnout=base_hist,
        literacy_rate=base_lit,
        awareness_score=base_aware,
        transport_accessibility=base_trans,
        weather_score=base_weather,
        campaign_intensity=base_campaign,
        holiday_factor=base_holiday,
        region_type=base_type
    )[0:3]
    
    # 2. Simulated values (applying boosts)
    sim_aware = min(100, base_aware + boost_awareness)
    sim_trans = min(100, base_trans + boost_transport)
    sim_weather = max(0, min(100, base_weather + adjust_weather))
    
    # Holiday adjustment logic
    if adjust_holiday == 'apply_holiday':
        sim_holiday = 1
    elif adjust_holiday == 'remove_holiday':
        sim_holiday = 0
    else:
        sim_holiday = base_holiday
        
    # Predict new final turnout using models
    sim_pred_turnout, sim_risk_label, _ = data_service.predict_region(
        historical_turnout=base_hist,
        literacy_rate=base_lit,
        awareness_score=sim_aware,
        transport_accessibility=sim_trans,
        weather_score=sim_weather,
        campaign_intensity=base_campaign,
        holiday_factor=sim_holiday,
        region_type=base_type
    )[0:3]
    
    # 3. Deltas & Formatting
    delta = sim_pred_turnout - base_pred_turnout
    delta_text = f"{'+' if delta >= 0 else ''}{delta:.2f}%"
    delta_style = {'color': '#22C55E' if delta >= 0 else '#EF4444', 'fontWeight': 'bold'}
    
    # Risk colors
    risk_colors = {'High': 'badge bg-danger', 'Medium': 'badge bg-warning', 'Low': 'badge bg-success'}
    base_badge_class = risk_colors.get(base_risk_label, 'badge bg-secondary')
    new_badge_class = risk_colors.get(sim_risk_label, 'badge bg-secondary')
    
    # Metrics display text
    aware_display = f"{base_aware} -> {sim_aware} (+{boost_awareness})" if boost_awareness > 0 else f"{base_aware}"
    trans_display = f"{base_trans} -> {sim_trans} (+{boost_transport})" if boost_transport > 0 else f"{base_trans}"
    weather_display = f"{base_weather} -> {sim_weather} ({adjust_weather:+.0f})" if adjust_weather != 0 else f"{base_weather}"
    
    # 4. Bar plot comparison
    comp_fig = go.Figure()
    comp_fig.add_trace(go.Bar(
        x=['Historical Baseline', 'AI Base Forecast', 'Simulated Forecast'],
        y=[base_hist, base_pred_turnout, sim_pred_turnout],
        marker_color=['#94A3B8', '#2563EB', '#22C55E' if delta >= 0 else '#EF4444'],
        text=[f"{base_hist}%", f"{base_pred_turnout}%", f"{sim_pred_turnout}%"],
        textposition='auto'
    ))
    comp_fig.update_layout(
        title=dict(text="Voter Turnout Simulation Comparison", font=dict(color='#F8FAFC', family='Poppins')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        yaxis=dict(gridcolor='#1E293B', title="Turnout Rate (%)", range=[30, 100]),
        margin=dict(l=45, r=20, t=40, b=40)
    )
    
    return (
        f"{base_pred_turnout}%", base_risk_label, base_badge_class,
        f"{sim_pred_turnout}%", sim_risk_label, new_badge_class,
        delta_text, delta_style,
        aware_display, trans_display, weather_display,
        comp_fig
    )
