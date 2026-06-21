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

PAGE_TRANSLATIONS = {
    'en': {
        'title': "What-If Operational Scenario Lab",
        'subtitle': "Simulate variations in weather conditions and test intervention policies to forecast turnout changes.",
        'state_lbl': "Select State",
        'district_lbl': "Select District",
        'constituency_lbl': "Select Constituency Cell",
        'scenarios_header': "Election Scenario Library™",
        'scenarios_rain': "🌧️ Torrential Rain / Extreme Heat",
        'scenarios_campaign': "📢 Intense Awareness Drive",
        'scenarios_holiday': "📅 Holiday Drag Effect",
        'scenarios_midweek': "🚀 Midweek Transit Mobilization",
        'adjustments_header': "Simulate Operational Adjustments",
        'awareness_slider': "Awareness Campaign Boost (0% to +30%)",
        'transport_slider': "Transport Shuttle Access Improvement (0% to +30%)",
        'weather_slider': "Weather Severity Adjustment (Rain/Heat) (-30% to +10%)",
        'holiday_slider': "Holiday Proximity Impact Toggle",
        'holiday_keep': "No Proximity Weekend (No Change)",
        'holiday_apply': "Simulate Near 3-Day Weekend (Apply Holiday Drag)",
        'holiday_remove': "Simulate Isolated Midweek Election (Apply Boost)",
        'btn_reset': "Reset to Region Baseline",
        'delta_header': "Simulation Forecast Delta",
        'base_forecast': "Baseline Forecast",
        'sim_forecast': "Simulated Forecast",
        'est_impact': "Estimated Impact",
        'proj_change': "Projected change",
        'awareness_score': "Awareness Score",
        'transport_score': "Transport Score",
        'weather_score': "Weather Score",
        'chart_title': "Voter Turnout Simulation Comparison",
        'chart_y_title': "Turnout Rate (%)",
        'lbl_historical': "Historical Baseline",
        'lbl_base_forecast': "AI Base Forecast",
        'lbl_sim_forecast': "Simulated Forecast",
        'high': "High",
        'medium': "Medium",
        'low': "Low",
        'n_a': "N/A"
    },
    'hi': {
        'title': "व्हाट-इफ ऑपरेशनल सिनेरियो लैब",
        'subtitle': "मतदान में होने वाले परिवर्तनों का पूर्वानुमान लगाने के लिए मौसम की स्थिति में बदलाव का अनुकरण करें और हस्तक्षेप नीतियों का परीक्षण करें।",
        'state_lbl': "राज्य चुनें",
        'district_lbl': "जिला चुनें",
        'constituency_lbl': "निर्वाचन क्षेत्र चुनें",
        'scenarios_header': "चुनाव परिदृश्य लाइब्रेरी™",
        'scenarios_rain': "🌧️ मूसलाधार बारिश / अत्यधिक गर्मी",
        'scenarios_campaign': "📢 गहन जागरूकता अभियान",
        'scenarios_holiday': "📅 छुट्टी का खिंचाव प्रभाव",
        'scenarios_midweek': "🚀 मध्य सप्ताह परिवहन गतिशीलता",
        'adjustments_header': "परिचालन समायोजन का अनुकरण करें",
        'awareness_slider': "जागरूकता अभियान में वृद्धि (0% से +30%)",
        'transport_slider': "परिवहन शटल पहुंच में सुधार (0% से +30%)",
        'weather_slider': "मौसम की तीव्रता समायोजन (बारिश/गर्मी) (-30% से +10%)",
        'holiday_slider': "छुट्टी की निकटता प्रभाव टॉगल",
        'holiday_keep': "कोई निकटता सप्ताहांत नहीं (कोई बदलाव नहीं)",
        'holiday_apply': "3-दिवसीय लंबे सप्ताहांत का अनुकरण करें (छुट्टी का प्रभाव लागू करें)",
        'holiday_remove': "अलग मध्य सप्ताह चुनाव का अनुकरण करें (बढ़ावा लागू करें)",
        'btn_reset': "क्षेत्र के आधारभूत मूल्य पर रीसेट करें",
        'delta_header': "सिमुलेशन पूर्वानुमान अंतर (Delta)",
        'base_forecast': "आधारभूत पूर्वानुमान",
        'sim_forecast': "सिम्युलेटेड पूर्वानुमान",
        'est_impact': "अनुमानित प्रभाव",
        'proj_change': "अनुमानित परिवर्तन",
        'awareness_score': "जागरूकता स्कोर",
        'transport_score': "परिवहन स्कोर",
        'weather_score': "मौसम स्कोर",
        'chart_title': "मतदाता मतदान सिमुलेशन तुलना",
        'chart_y_title': "मतदान दर (%)",
        'lbl_historical': "ऐतिहासिक आधारभूत रेखा",
        'lbl_base_forecast': "एआई आधारभूत पूर्वानुमान",
        'lbl_sim_forecast': "सिम्युलेटेड पूर्वानुमान",
        'high': "उच्च",
        'medium': "मध्यम",
        'low': "निम्न",
        'n_a': "लागू नहीं"
    },
    'kn': {
        'title': "ವಾಟ್-ಇಫ್ ಕಾರ್ಯಾಚರಣೆಯ ಸಿಮ್ಯುಲೇಶನ್ ಲ್ಯಾಬ್",
        'subtitle': "ಮತದಾನದ ಬದಲಾವಣೆಗಳನ್ನು ಮುನ್ಸೂಚಿಸಲು ಹವಾಮಾನ ಪರಿಸ್ಥಿತಿಗಳಲ್ಲಿನ ವ್ಯತ್ಯಾಸಗಳನ್ನು ಸಿಮ್ಯುಲೇಟ್ ಮಾಡಿ ಮತ್ತು ನೀತಿಗಳನ್ನು ಪರೀಕ್ಷಿಸಿ.",
        'state_lbl': "ರಾಜ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        'district_lbl': "ಜಿಲ್ಲೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        'constituency_lbl': "ಮತಕ್ಷೇತ್ರವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        'scenarios_header': "ಚುನಾವಣಾ ಸನ್ನಿವೇಶ ಲೈಬ್ರರಿ™",
        'scenarios_rain': "🌧️ ವಿಪರೀತ ಮಳೆ / ತೀವ್ರ ಬಿಸಿಲು",
        'scenarios_campaign': "📢 ತೀವ್ರ ಜಾಗೃತಿ ಅಭಿಯಾನ",
        'scenarios_holiday': "📅 ರಜಾದಿನದ ಡ್ರ್ಯಾಗ್ ಪರಿಣಾಮ",
        'scenarios_midweek': "🚀 ವಾರದ ಮಧ್ಯದ ಸಾರಿಗೆ ಸಜ್ಜುಗೊಳಿಸುವಿಕೆ",
        'adjustments_header': "ಕಾರ್ಯಾಚರಣೆಯ ಹೊಂದಾಣಿಕೆಗಳನ್ನು ಸಿಮ್ಯುಲೇಟ್ ಮಾಡಿ",
        'awareness_slider': "ಜಾಗೃತಿ ಅಭಿಯಾನದ ಹೆಚ್ಚಳ (0% ರಿಂದ +30%)",
        'transport_slider': "ಸಾರಿಗೆ ಶಟಲ್ ಪ್ರವೇಶದ ಸುಧಾರಣೆ (0% ರಿಂದ +30%)",
        'weather_slider': "ಹವಾಮಾನ ತೀವ್ರತೆಯ ಹೊಂದಾಣಿಕೆ (ಮಳೆ/ಬಿಸಿಲು) (-30% ರಿಂದ +10%)",
        'holiday_slider': "ರಜಾದಿನದ ಸಾಮೀಪ್ಯದ ಪ್ರಭಾವದ ಟಾಗಲ್",
        'holiday_keep': "ರಜೆಯಿಲ್ಲದ ವಾರಾಂತ್ಯ (ಬದಲಾವಣೆ ಇಲ್ಲ)",
        'holiday_apply': "3 ದಿನಗಳ ವಾರಾಂತ್ಯದ ಸಿಮ್ಯುಲೇಶನ್ (ರಜಾದಿನದ ಡ್ರ್ಯಾಗ್ ಅನ್ವಯಿಸಿ)",
        'holiday_remove': "ಪ್ರತ್ಯೇಕ ವಾರದ ಮಧ್ಯದ ಚುನಾವಣೆಯ ಸಿಮ್ಯುಲೇಶನ್ (ಬೂಸ್ಟ್ ಅನ್ವಯಿಸಿ)",
        'btn_reset': "ಪ್ರದೇಶದ ಬೇಸ್‌ಲೈನ್‌ಗೆ ಮರುಹೊಂದಿಸಿ",
        'delta_header': "ಸಿಮ್ಯುಲೇಶನ್ ಮುನ್ಸೂಚನೆಯ ವ್ಯತ್ಯಾಸ",
        'base_forecast': "ಬೇಸ್‌ಲೈನ್ ಮುನ್ಸೂಚನೆ",
        'sim_forecast': "ಸಿಮ್ಯುಲೇಟೆಡ್ ಮುನ್ಸೂಚನೆ",
        'est_impact': "ನಿರೀಕ್ಷಿತ ಪ್ರಭಾವ",
        'proj_change': "ಯೋಜಿತ ಬದಲಾವಣೆ",
        'awareness_score': "ಜಾಗೃತಿ ಸ್ಕೋರ್",
        'transport_score': "ಸಾರಿಗೆ ಸ್ಕೋರ್",
        'weather_score': "ಹವಾಮಾನ ಸ್ಕೋರ್",
        'chart_title': "ಮತದಾರರ ಮತದಾನದ ಸಿಮ್ಯುಲೇಶನ್ ಹೋಲಿಕೆ",
        'chart_y_title': "ಮತದಾನದ ಪ್ರಮಾಣ (%)",
        'lbl_historical': "ಐತಿಹಾಸಿಕ ಬೇಸ್‌ಲೈನ್",
        'lbl_base_forecast': "ಎಐ ಬೇಸ್ ಮುನ್ಸೂಚನೆ",
        'lbl_sim_forecast': "ಸಿಮ್ಯುಲೇಟೆಡ್ ಮುನ್ಸೂಚನೆ",
        'high': "ಹೆಚ್ಚು",
        'medium': "ಮಧ್ಯಮ",
        'low': "ಕಡಿಮೆ",
        'n_a': "ಲಭ್ಯವಿಲ್ಲ"
    }
}

def get_layout(lang='en'):
    t = PAGE_TRANSLATIONS.get(lang, PAGE_TRANSLATIONS['en'])
    states = data_service.get_states()
    state_options = [{'label': s, 'value': s} for s in states]
    
    # Preset Selector Section
    selector_card = dbc.Card([
        dbc.Row([
            dbc.Col([
                html.Label(t['state_lbl'], className="form-label-custom"),
                dcc.Dropdown(
                    id='sim-state-select',
                    options=state_options,
                    value=states[0] if states else None,
                    clearable=False,
                    className="bg-dark text-white border-secondary"
                )
            ], md=4),
            dbc.Col([
                html.Label(t['district_lbl'], className="form-label-custom"),
                dcc.Dropdown(
                    id='sim-district-select',
                    options=[],
                    clearable=False,
                    className="bg-dark text-white border-secondary"
                )
            ], md=4),
            dbc.Col([
                html.Label(t['constituency_lbl'], className="form-label-custom"),
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
        html.H6(t['scenarios_header'], className="mb-3", style={'fontFamily': 'Poppins', 'color': '#F8FAFC', 'fontSize': '0.9rem'}),
        html.Div([
            dbc.Button(t['scenarios_rain'], id='preset-rain', color="danger", size="sm", className="me-2 mb-2", style={'fontSize': '0.75rem', 'fontWeight': '500'}),
            dbc.Button(t['scenarios_campaign'], id='preset-campaign-boost', color="success", size="sm", className="me-2 mb-2", style={'fontSize': '0.75rem', 'fontWeight': '500'}),
            dbc.Button(t['scenarios_holiday'], id='preset-holiday-drag', color="warning", size="sm", className="me-2 mb-2", style={'fontSize': '0.75rem', 'fontWeight': '500'}),
            dbc.Button(t['scenarios_midweek'], id='preset-midweek', color="info", size="sm", className="me-2 mb-2", style={'fontSize': '0.75rem', 'fontWeight': '500'})
        ], className="d-flex flex-wrap")
    ], className="stat-card p-3 mb-3")

    # Sliders Card
    sliders_card = dbc.Card([
        html.H5(t['adjustments_header'], className="mb-4", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
        
        html.Div([
            html.Label(t['awareness_slider'], className="form-label-custom"),
            dcc.Slider(0, 30, 1, value=0, id='sim-boost-awareness', 
                       marks={0: '0', 10: '+10%', 20: '+20%', 30: '+30%'}, className="mb-4")
        ]),
        
        html.Div([
            html.Label(t['transport_slider'], className="form-label-custom"),
            dcc.Slider(0, 30, 1, value=0, id='sim-boost-transport', 
                       marks={0: '0', 10: '+10%', 20: '+20%', 30: '+30%'}, className="mb-4")
        ]),
        
        html.Div([
            html.Label(t['weather_slider'], className="form-label-custom"),
            dcc.Slider(-30, 10, 1, value=0, id='sim-adjust-weather', 
                       marks={-30: 'Extreme', -15: 'Harsh', 0: 'Baseline', 10: 'Pleasant'}, className="mb-4")
        ]),
        
        html.Div([
            html.Label(t['holiday_slider'], className="form-label-custom"),
            dcc.Dropdown(
                id='sim-adjust-holiday',
                options=[
                    {'label': t['holiday_keep'], 'value': 'keep'},
                    {'label': t['holiday_apply'], 'value': 'apply_holiday'},
                    {'label': t['holiday_remove'], 'value': 'remove_holiday'}
                ],
                value='keep',
                clearable=False,
                className="bg-dark text-white border-secondary mb-4"
            )
        ]),
        
        dbc.Button(t['btn_reset'], id='sim-reset-btn', color="secondary", className="w-100", style={'fontWeight': '600'})
    ], className="stat-card p-4 overflow-visible")

    # Outputs card
    outputs_panel = html.Div([
        # Comparison Gauges and metrics
        dbc.Card([
            html.H5(t['delta_header'], className="mb-4", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
            
            dbc.Row([
                dbc.Col([
                    html.Div(t['base_forecast'], style={'fontSize': '0.85rem', 'color': '#94A3B8'}),
                    html.Div(id='sim-out-base-turnout', style={'fontSize': '2rem', 'fontWeight': 'bold', 'color': '#94A3B8'}),
                    html.Div(id='sim-out-base-risk', className="badge bg-secondary", style={'fontSize': '0.75rem'})
                ], md=4, className="text-center mb-3"),
                
                dbc.Col([
                    html.Div(t['sim_forecast'], style={'fontSize': '0.85rem', 'color': '#94A3B8'}),
                    html.Div(id='sim-out-new-turnout', style={'fontSize': '2.6rem', 'fontWeight': 'bold', 'color': '#60A5FA'}),
                    html.Div(id='sim-out-new-risk', className="badge bg-primary", style={'fontSize': '0.85rem'})
                ], md=4, className="text-center border-start border-end border-secondary mb-3"),
                
                dbc.Col([
                    html.Div(t['est_impact'], style={'fontSize': '0.85rem', 'color': '#94A3B8'}),
                    html.Div(id='sim-out-delta', style={'fontSize': '2.2rem', 'fontWeight': 'bold', 'color': '#22C55E'}),
                    html.Div(t['proj_change'], style={'fontSize': '0.75rem', 'color': '#94A3B8'})
                ], md=4, className="text-center mb-3")
            ], className="align-items-center mb-3"),
            
            html.Hr(style={'borderColor': '#1E293B'}),
            
            # Sub-indicators
            dbc.Row([
                dbc.Col([
                    html.Div(t['awareness_score'], style={'fontSize': '0.75rem', 'color': '#94A3B8'}),
                    html.Div(id='sim-out-awareness-val', style={'fontWeight': 'bold', 'color': '#F8FAFC'})
                ], xs=4, className="text-center"),
                dbc.Col([
                    html.Div(t['transport_score'], style={'fontSize': '0.75rem', 'color': '#94A3B8'}),
                    html.Div(id='sim-out-transport-val', style={'fontWeight': 'bold', 'color': '#F8FAFC'})
                ], xs=4, className="text-center"),
                dbc.Col([
                    html.Div(t['weather_score'], style={'fontSize': '0.75rem', 'color': '#94A3B8'}),
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
            html.H3(t['title'], style={'fontFamily': 'Poppins', 'fontWeight': '600', 'color': '#F8FAFC'}),
            html.P(t['subtitle'], style={'color': '#94A3B8'})
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
    State('sim-district-select', 'value'),
    State('lang-store', 'data')
)
def run_what_if_simulation(constituency, boost_awareness, boost_transport, adjust_weather, adjust_holiday, state, district, lang):
    if not lang:
        lang = 'en'
    t = PAGE_TRANSLATIONS.get(lang, PAGE_TRANSLATIONS['en'])

    if not constituency:
        return t['n_a'], t['n_a'], "badge bg-secondary", t['n_a'], t['n_a'], "badge bg-secondary", "0.00%", {'color': '#94A3B8'}, t['n_a'], t['n_a'], t['n_a'], go.Figure()
        
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
    
    # Risk colors & translations
    risk_colors = {'High': 'badge bg-danger', 'Medium': 'badge bg-warning', 'Low': 'badge bg-success'}
    base_badge_class = risk_colors.get(base_risk_label, 'badge bg-secondary')
    new_badge_class = risk_colors.get(sim_risk_label, 'badge bg-secondary')
    
    t_base_risk = t[base_risk_label.lower()]
    t_sim_risk = t[sim_risk_label.lower()]
    
    # Metrics display text
    aware_display = f"{base_aware} -> {sim_aware} (+{boost_awareness})" if boost_awareness > 0 else f"{base_aware}"
    trans_display = f"{base_trans} -> {sim_trans} (+{boost_transport})" if boost_transport > 0 else f"{base_trans}"
    weather_display = f"{base_weather} -> {sim_weather} ({adjust_weather:+.0f})" if adjust_weather != 0 else f"{base_weather}"
    
    # 4. Bar plot comparison
    comp_fig = go.Figure()
    comp_fig.add_trace(go.Bar(
        x=[t['lbl_historical'], t['lbl_base_forecast'], t['lbl_sim_forecast']],
        y=[base_hist, base_pred_turnout, sim_pred_turnout],
        marker_color=['#94A3B8', '#2563EB', '#22C55E' if delta >= 0 else '#EF4444'],
        text=[f"{base_hist}%", f"{base_pred_turnout}%", f"{sim_pred_turnout}%"],
        textposition='auto'
    ))
    comp_fig.update_layout(
        title=dict(text=t['chart_title'], font=dict(color='#F8FAFC', family='Poppins')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        yaxis=dict(gridcolor='#1E293B', title=t['chart_y_title'], range=[30, 100]),
        margin=dict(l=45, r=20, t=40, b=40)
    )
    
    return (
        f"{base_pred_turnout}%", t_base_risk, base_badge_class,
        f"{sim_pred_turnout}%", t_sim_risk, new_badge_class,
        delta_text, delta_style,
        aware_display, trans_display, weather_display,
        comp_fig
    )
