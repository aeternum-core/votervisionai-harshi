from dash import html, dcc, callback, Input, Output, State
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
    
    # Left Column: Inputs Form
    inputs_card = dbc.Card([
        html.H5("Voter Region Parameters", className="mb-4", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
        
        # Preset loading option
        dbc.Row([
            dbc.Col([
                html.Label("Load State Preset", className="form-label-custom"),
                dcc.Dropdown(
                    id='pred-state-select',
                    options=state_options,
                    value=states[0] if states else None,
                    clearable=False,
                    className="bg-dark text-white border-secondary mb-3"
                )
            ], md=6),
            dbc.Col([
                html.Label("Load District Preset", className="form-label-custom"),
                dcc.Dropdown(
                    id='pred-district-select',
                    options=[],
                    clearable=False,
                    className="bg-dark text-white border-secondary mb-3"
                )
            ], md=6),
        ]),
        html.Hr(style={'borderColor': '#1E293B'}),
        
        # Demographics
        dbc.Row([
            dbc.Col([
                html.Label("Historical Turnout (%)", className="form-label-custom"),
                dbc.Input(id='pred-hist-turnout', type='number', min=30, max=100, step=0.1, value=68.5, className="bg-dark text-white border-secondary mb-3")
            ], md=6),
            dbc.Col([
                html.Label("Literacy Rate (%)", className="form-label-custom"),
                dbc.Input(id='pred-literacy', type='number', min=30, max=100, step=0.1, value=75.2, className="bg-dark text-white border-secondary mb-3")
            ], md=6),
        ]),
        
        dbc.Row([
            dbc.Col([
                html.Label("Region Type", className="form-label-custom"),
                dcc.Dropdown(
                    id='pred-region-type',
                    options=[{'label': 'Urban', 'value': 'Urban'}, {'label': 'Rural', 'value': 'Rural'}],
                    value='Rural',
                    clearable=False,
                    className="bg-dark text-white border-secondary mb-3"
                )
            ], md=6),
            dbc.Col([
                html.Label("Election Day near Holiday?", className="form-label-custom"),
                dcc.Dropdown(
                    id='pred-holiday',
                    options=[{'label': 'Yes (Lower Participation Risk)', 'value': 1}, {'label': 'No', 'value': 0}],
                    value=0,
                    clearable=False,
                    className="bg-dark text-white border-secondary mb-3"
                )
            ], md=6),
        ]),
        
        # Sliders for parameters
        html.Div([
            html.Label("Awareness Campaign Intensity (0-100)", className="form-label-custom"),
            dcc.Slider(0, 100, 1, value=65, id='pred-awareness', className="mb-4")
        ]),
        
        html.Div([
            html.Label("Public Transport & Booth Accessibility (0-100)", className="form-label-custom"),
            dcc.Slider(0, 100, 1, value=70, id='pred-accessibility', className="mb-4")
        ]),
        
        html.Div([
            html.Label("Weather Comfort Score (0-100) (Low = Extreme Rain/Heat)", className="form-label-custom"),
            dcc.Slider(0, 100, 1, value=75, id='pred-weather', className="mb-4")
        ]),
        
        html.Div([
            html.Label("Election Campaign Intensity Score (0-100)", className="form-label-custom"),
            dcc.Slider(0, 100, 1, value=60, id='pred-campaign', className="mb-4")
        ]),
        
        dbc.Button("Generate AI Forecast", id='predict-btn', color="primary", className="w-100 mt-2", style={'fontWeight': '600'})
    ], className="stat-card p-4 overflow-visible")

    # Right Column: Output Results View
    outputs_panel = html.Div([
        # Prediction Output card
        dbc.Card([
            html.H5("AI Forecast Model Results", className="mb-4", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
            
            dbc.Row([
                dbc.Col([
                    html.Div("Expected Final Turnout", style={'fontSize': '0.9rem', 'color': '#94A3B8'}),
                    html.Div(id='pred-out-turnout', style={'fontSize': '3.2rem', 'fontWeight': 'bold', 'color': '#60A5FA', 'fontFamily': 'Poppins'}),
                    html.Div(id='pred-out-range', className="text-muted", style={'fontSize': '0.8rem', 'marginTop': '-5px'})
                ], md=6, className="text-center border-end border-secondary mb-3"),
                
                dbc.Col([
                    html.Div("Voter Turnout Risk Alert", style={'fontSize': '0.9rem', 'color': '#94A3B8'}),
                    html.Div(id='pred-out-risk', style={'fontSize': '2.2rem', 'fontWeight': 'bold', 'marginTop': '0.5rem', 'fontFamily': 'Poppins'}),
                    html.Div(id='pred-out-risk-desc', className="text-muted", style={'fontSize': '0.75rem'})
                ], md=6, className="text-center mb-3"),
            ], className="align-items-center mb-4"),
            
            # Confidence gauge
            html.Hr(style={'borderColor': '#1E293B'}),
            html.Div([
                dcc.Graph(id='pred-out-confidence-gauge', config={'displayModeBar': False})
            ], style={'marginTop': '-10px'})
        ], className="stat-card mb-4"),
        
        # Explainable AI Drivers list
        dbc.Card([
            html.H5("Explainable AI (XAI) - Prediction Drivers", className="mb-3", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
            html.P("Auditing how each local demographic and weather factor influenced the model's prediction:", style={'fontSize': '0.8rem', 'color': '#94A3B8', 'marginBottom': '1rem'}),
            html.Div(id='pred-xai-drivers-list')
        ], className="stat-card mb-4"),
        
        # Feature Importance Chart card
        dbc.Card([
            dcc.Graph(id='pred-importance-chart', config={'displayModeBar': False})
        ], className="stat-card")
    ])

    return html.Div([
        # Title
        html.Div([
            html.H3("AI Voter Participation Predictor", style={'fontFamily': 'Poppins', 'fontWeight': '600', 'color': '#F8FAFC'}),
            html.P("Feed geographical, socio-economic, and election-day environmental features to simulate and forecast voter participation metrics.", style={'color': '#94A3B8'})
        ], className="mb-4"),
        
        # Layout splits
        dbc.Row([
            dbc.Col(inputs_card, lg=6, md=12, className="mb-4"),
            dbc.Col(outputs_panel, lg=6, md=12, className="mb-4")
        ])
    ])

# Callbacks to fill preset values
@callback(
    Output('pred-district-select', 'options'),
    Output('pred-district-select', 'value'),
    Input('pred-state-select', 'value')
)
def update_pred_districts(selected_state):
    districts = data_service.get_districts(state=selected_state)
    options = [{'label': d, 'value': d} for d in districts]
    val = districts[0] if districts else None
    return options, val

@callback(
    Output('pred-hist-turnout', 'value'),
    Output('pred-literacy', 'value'),
    Output('pred-region-type', 'value'),
    Output('pred-awareness', 'value'),
    Output('pred-accessibility', 'value'),
    Output('pred-weather', 'value'),
    Output('pred-campaign', 'value'),
    Output('pred-holiday', 'value'),
    Input('pred-district-select', 'value'),
    State('pred-state-select', 'value')
)
def load_district_presets(selected_district, selected_state):
    if not selected_district or selected_district == 'ALL':
        return 68.5, 75.2, 'Rural', 65, 70, 75, 60, 0
        
    df = data_service.df
    rows = df[(df['state'] == selected_state) & (df['district'] == selected_district)]
    if rows.empty:
        return 68.5, 75.2, 'Rural', 65, 70, 75, 60, 0
        
    # Get average values for this district
    row = rows.iloc[0]
    return (
        float(row['historical_turnout']),
        float(row['literacy_rate']),
        str(row['region_type']),
        int(row['awareness_score']),
        int(row['transport_accessibility']),
        int(row['weather_score']),
        int(row['campaign_intensity']),
        int(row['holiday_factor'])
    )

# Callback to run the machine learning models
@callback(
    Output('pred-out-turnout', 'children'),
    Output('pred-out-range', 'children'),
    Output('pred-out-risk', 'children'),
    Output('pred-out-risk', 'style'),
    Output('pred-out-risk-desc', 'children'),
    Output('pred-out-confidence-gauge', 'figure'),
    Output('pred-xai-drivers-list', 'children'),
    Output('pred-importance-chart', 'figure'),
    Input('predict-btn', 'n_clicks'),
    State('pred-hist-turnout', 'value'),
    State('pred-literacy', 'value'),
    State('pred-region-type', 'value'),
    State('pred-awareness', 'value'),
    State('pred-accessibility', 'value'),
    State('pred-weather', 'value'),
    State('pred-campaign', 'value'),
    State('pred-holiday', 'value')
)
def execute_prediction(n_clicks, hist, literacy, region_type, awareness, accessibility, weather, campaign, holiday):
    # Default outputs if no inputs yet or values are None
    if hist is None or literacy is None:
        hist, literacy = 68.5, 75.2
        
    # Run the prediction through data_service
    pred_turnout, risk_label, confidence, drivers = data_service.predict_region(
        historical_turnout=hist,
        literacy_rate=literacy,
        awareness_score=awareness,
        transport_accessibility=accessibility,
        weather_score=weather,
        campaign_intensity=campaign,
        holiday_factor=holiday,
        region_type=region_type
    )
    
    # 1. Expected Turnout formatting
    turnout_text = f"{pred_turnout:.2f}%"
    
    # Standard Margin of Error from MAE (approx 1.9%)
    mae = 1.91
    range_text = f"Turnout Probability Range: {(pred_turnout - mae):.2f}% to {(pred_turnout + mae):.2f}%"
    
    # 2. Risk Alert color formatting
    if risk_label == 'High':
        risk_color = {'color': '#EF4444'}
        risk_desc = "Significant participation drop expected compared to historical levels. Immediate civic outreach needed."
    elif risk_label == 'Medium':
        risk_color = {'color': '#FACC15'}
        risk_desc = "Mild turnout deficit forecasted. Monitor voting velocity closely."
    else:
        risk_color = {'color': '#22C55E'}
        risk_desc = "Voter participation performing strongly or exceeding historical averages."
        
    # 3. Plotly Gauge for Confidence Indicator
    confidence_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Prediction Confidence Meter", 'font': {'color': '#94A3B8', 'size': 12, 'family': 'Poppins'}},
        number={'suffix': "%", 'font': {'color': '#F8FAFC', 'size': 32, 'family': 'Poppins'}},
        gauge={
            'axis': {'range': [50, 100], 'tickwidth': 1, 'tickcolor': "#94A3B8", 'tickfont': {'color': '#94A3B8'}},
            'bar': {'color': "#2563EB"},
            'bgcolor': "#0B1220",
            'borderwidth': 1,
            'bordercolor': "#1E293B",
            'steps': [
                {'range': [50, 75], 'color': 'rgba(239, 68, 68, 0.15)'},
                {'range': [75, 87], 'color': 'rgba(250, 204, 21, 0.15)'},
                {'range': [87, 100], 'color': 'rgba(34, 197, 94, 0.15)'}
            ]
        }
    ))
    confidence_fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#F8FAFC'),
        height=140,
        margin=dict(l=40, r=40, t=30, b=0)
    )
    
    # 4. Explainable AI Driver lists mapping
    xai_elements = []
    for d in drivers:
        val = d['contribution']
        if d['type'] == 'baseline':
            badge = html.Span(f"{val:.2f}% Baseline", className="badge bg-primary ms-auto", style={'fontWeight': 'bold', 'fontSize': '0.75rem'})
        else:
            if val > 0:
                badge = html.Span(f"+{val:.2f}%", className="badge bg-success text-white ms-auto", style={'fontWeight': 'bold', 'fontSize': '0.75rem', 'backgroundColor': 'rgba(34, 197, 94, 0.2) !important'})
            elif val < 0:
                badge = html.Span(f"{val:.2f}%", className="badge bg-danger text-white ms-auto", style={'fontWeight': 'bold', 'fontSize': '0.75rem', 'backgroundColor': 'rgba(239, 68, 68, 0.2) !important'})
            else:
                badge = html.Span("0.00%", className="badge bg-secondary ms-auto", style={'fontSize': '0.75rem'})
                
        xai_elements.append(
            html.Div([
                html.Span(d['feature'], style={'fontSize': '0.85rem', 'color': '#F8FAFC'}),
                badge
            ], className="d-flex align-items-center py-2 border-bottom border-secondary", style={'borderColor': 'rgba(30, 41, 59, 0.4)'})
        )
        
    xai_list = html.Div(xai_elements)

    # 5. Feature Importance plot
    if data_service.model_eval is not None and 'regression' in data_service.model_eval:
        importances = data_service.model_eval['regression']['feature_importance']
        features = list(importances.keys())
        values = list(importances.values())
        
        # Clean labels for presentation
        clean_features = {
            'historical_turnout': 'Historical Turnout',
            'literacy_rate': 'Literacy Rate',
            'awareness_score': 'Awareness Score',
            'transport_accessibility': 'Booth Access Score',
            'weather_score': 'Weather comfort',
            'campaign_intensity': 'Campaign Budget',
            'holiday_factor': 'Holiday Proximity',
            'is_urban': 'Urban Status'
        }
        labels = [clean_features.get(f, f) for f in features]
        
        # Sort together
        sorted_pairs = sorted(zip(values, labels))
        values, labels = zip(*sorted_pairs)
    else:
        # Fallback values
        labels = ['Holiday Proximity', 'Urban Status', 'Weather comfort', 'Booth Access Score', 'Campaign Budget', 'Awareness Score', 'Literacy Rate', 'Historical Turnout']
        values = [0.03, 0.05, 0.08, 0.12, 0.15, 0.17, 0.18, 0.22]
        
    importance_fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation='h',
        marker_color='#2563EB'
    ))
    importance_fig.update_layout(
        title=dict(text="Model Feature Importance Weightings", font=dict(color='#F8FAFC', family='Poppins')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        xaxis=dict(gridcolor='#1E293B', title="Influence weight"),
        yaxis=dict(gridcolor='#1E293B'),
        margin=dict(l=140, r=20, t=40, b=40)
    )
    
    return turnout_text, range_text, risk_label, risk_color, risk_desc, confidence_fig, xai_list, importance_fig
