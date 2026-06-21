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

PAGE_TRANSLATIONS = {
    'en': {
        'title': 'AI Voter Participation Predictor',
        'subtitle': "Feed geographical, socio-economic, and election-day environmental features to simulate and forecast voter participation metrics.",
        'params_header': "Voter Region Parameters",
        'preset_state': "Load State Preset",
        'preset_district': "Load District Preset",
        'hist_turnout': "Historical Turnout (%)",
        'literacy': "Literacy Rate (%)",
        'region_type': "Region Type",
        'holiday': "Election Day near Holiday?",
        'holiday_yes': "Yes (Lower Participation Risk)",
        'holiday_no': "No",
        'awareness': "Awareness Campaign Intensity (0-100)",
        'accessibility': "Public Transport & Booth Accessibility (0-100)",
        'weather': "Weather Comfort Score (0-100) (Low = Extreme Rain/Heat)",
        'campaign': "Election Campaign Intensity Score (0-100)",
        'btn_forecast': "Generate AI Forecast",
        'results_header': "AI Forecast Model Results",
        'expected_turnout': "Expected Final Turnout",
        'risk_alert': "Voter Turnout Risk Alert",
        'xai_header': "Explainable AI (XAI) - Prediction Drivers",
        'xai_desc': "Auditing how each local demographic and weather factor influenced the model's prediction:",
        'chart_importance': "Model Feature Importance Weightings",
        'influence_weight': "Influence weight",
        'gauge_title': "Prediction Confidence Meter",
        'urban': "Urban",
        'rural': "Rural",
        'high': "High",
        'medium': "Medium",
        'low': "Low",
        'n_a': "N/A",
        'baseline_txt': "Baseline",
        'range_text_fmt': "Turnout Probability Range: {min_val:.2f}% to {max_val:.2f}%",
        'risk_desc_high': "Significant participation drop expected compared to historical levels. Immediate civic outreach needed.",
        'risk_desc_medium': "Mild turnout deficit forecasted. Monitor voting velocity closely.",
        'risk_desc_low': "Voter participation performing strongly or exceeding historical averages."
    },
    'hi': {
        'title': 'एआई मतदाता भागीदारी पूर्वानुमानकर्ता',
        'subtitle': "मतदाता भागीदारी मेट्रिक्स का अनुकरण और पूर्वानुमान करने के लिए भौगोलिक, सामाजिक-आर्थिक और चुनाव-दिन की पर्यावरणीय विशेषताओं को इनपुट करें।",
        'params_header': "मतदाता क्षेत्र के मापदंड",
        'preset_state': "राज्य प्रीसेट लोड करें",
        'preset_district': "जिला प्रीसेट लोड करें",
        'hist_turnout': "ऐतिहासिक मतदान (%)",
        'literacy': "साक्षरता दर (%)",
        'region_type': "क्षेत्र का प्रकार",
        'holiday': "क्या चुनाव का दिन छुट्टी के पास है?",
        'holiday_yes': "हाँ (कम भागीदारी का जोखिम)",
        'holiday_no': "नहीं",
        'awareness': "जागरूकता अभियान की तीव्रता (0-100)",
        'accessibility': "सार्वजनिक परिवहन और बूथ सुलभता (0-100)",
        'weather': "मौसम आराम स्कोर (0-100) (कम = अत्यधिक बारिश/गर्मी)",
        'campaign': "चुनाव प्रचार तीव्रता स्कोर (0-100)",
        'btn_forecast': "एआई पूर्वानुमान उत्पन्न करें",
        'results_header': "एआई पूर्वानुमान मॉडल के परिणाम",
        'expected_turnout': "अपेक्षित अंतिम मतदान",
        'risk_alert': "मतदाता मतदान जोखिम चेतावनी",
        'xai_header': "व्याख्यात्मक एआई (XAI) - पूर्वानुमान चालक",
        'xai_desc': "ऑडिट करना कि प्रत्येक स्थानीय जनसांख्यिकीय और मौसम कारक ने मॉडल के पूर्वानुमान को कैसे प्रभावित किया:",
        'chart_importance': "मॉडल विशेषता महत्व भार",
        'influence_weight': "प्रभाव भार",
        'gauge_title': "पूर्वानुमान आत्मविश्वास मीटर",
        'urban': "शहरी",
        'rural': "ग्रामीण",
        'high': "उच्च",
        'medium': "मध्यम",
        'low': "निम्न",
        'n_a': "लागू नहीं",
        'baseline_txt': "आधारभूत रेखा",
        'range_text_fmt': "मतदान संभाव्यता सीमा: {min_val:.2f}% से {max_val:.2f}%",
        'risk_desc_high': "ऐतिहासिक स्तरों की तुलना में महत्वपूर्ण मतदान गिरावट की उम्मीद है। तत्काल नागरिक आउटरीच की आवश्यकता है।",
        'risk_desc_medium': "हल्का मतदान घाटा पूर्वानुमानित है। मतदान की गति पर बारीकी से नज़र रखें।",
        'risk_desc_low': "मतदाता भागीदारी दृढ़ता से प्रदर्शन कर रही है या ऐतिहासिक औसत से अधिक है।"
    },
    'kn': {
        'title': 'ಎಐ ಮತದಾರರ ಭಾಗವಹಿಸುವಿಕೆ ಮುನ್ಸೂಚಕ',
        'subtitle': "ಮತದಾರರ ಭಾಗವಹಿಸುವಿಕೆಯ ಮೆಟ್ರಿಕ್‌ಗಳನ್ನು ಸಿಮ್ಯುಲೇಟ್ ಮಾಡಲು ಮತ್ತು ಮುನ್ಸೂಚಿಸಲು ಭೌಗೋಳಿಕ, ಸಾಮಾಜಿಕ-ಆರ್ಥಿಕ ಮತ್ತು ಚುನಾವಣಾ ದಿನದ ಪರಿಸರ ವೈಶಿಷ್ಟ್ಯಗಳನ್ನು ಒದಗಿಸಿ.",
        'params_header': "ಮತದಾರರ ಪ್ರದೇಶದ ನಿಯತಾಂಕಗಳು",
        'preset_state': "ರಾಜ್ಯ ಪ್ರಿಸೆಟ್ ಲೋಡ್ ಮಾಡಿ",
        'preset_district': "ಜಿಲ್ಲಾ ಪ್ರಿಸೆಟ್ ಲೋಡ್ ಮಾಡಿ",
        'hist_turnout': "ಐತಿಹಾಸಿಕ ಮತದಾನ (%)",
        'literacy': "ಸಾಕ್ಷರತಾ ಪ್ರಮಾಣ (%)",
        'region_type': "ಪ್ರದೇಶದ ಪ್ರಕಾರ",
        'holiday': "ಚುನಾವಣಾ ದಿನವು ರಜೆಯ ಸಮೀಪದಲ್ಲಿದೆಯೇ?",
        'holiday_yes': "ಹೌದು (ಕಡಿಮೆ ಭಾಗವಹಿಸುವಿಕೆ ಅಪಾಯ)",
        'holiday_no': "ಇಲ್ಲ",
        'awareness': "ಜಾಗೃತಿ ಅಭಿಯಾನದ ತೀವ್ರತೆ (0-100)",
        'accessibility': "ಸಾರ್ವಜನಿಕ ಸಾರಿಗೆ ಮತ್ತು ಮತಗಟ್ಟೆ ಪ್ರವೇಶಿಸುವಿಕೆ (0-100)",
        'weather': "ಹವಾಮಾನ ಕಂಫರ್ಟ್ ಸ್ಕೋರ್ (0-100) (ಕಡಿಮೆ = ವಿಪರೀತ ಮಳೆ/ಬಿಸಿಲು)",
        'campaign': "ಚುನಾವಣಾ ಪ್ರಚಾರ ತೀವ್ರತೆಯ ಸ್ಕೋರ್ (0-100)",
        'btn_forecast': "ಎಐ ಮುನ್ಸೂಚನೆ ರಚಿಸಿ",
        'results_header': "ಎಐ ಮುನ್ಸೂಚನೆ ಮಾದರಿಯ ಫಲಿತಾಂಶಗಳು",
        'expected_turnout': "ನಿರೀಕ್ಷಿತ ಅಂತಿಮ ಮತದಾನ",
        'risk_alert': "ಮತದಾರರ ಮತದಾನ ಅಪಾಯದ ಎಚ್ಚರಿಕೆ",
        'xai_header': "ವಿವರಣಾತ್ಮಕ ಎಐ (XAI) - ಮುನ್ಸೂಚನೆಯ ಪ್ರಮುಖ ಅಂಶಗಳು",
        'xai_desc': "ಪ್ರತಿಯೊಂದು ಸ್ಥಳೀಯ ಜನಸಂಖ್ಯಾ ಮತ್ತು ಹವಾಮಾನ ಅಂಶಗಳು ಮಾದರಿಯ ಮುನ್ಸೂಚನೆಯ ಮೇಲೆ ಹೇಗೆ ಪ್ರಭಾವ ಬೀರಿದೆ ಎಂಬುದನ್ನು ಪರಿಶೀಲಿಸುವುದು:",
        'chart_importance': "ಮಾದರಿ ವೈಶಿಷ್ಟ್ಯಗಳ ಪ್ರಾಮುಖ್ಯತೆಯ ತೂಕ",
        'influence_weight': "ಪ್ರಭಾವದ ತೂಕ",
        'gauge_title': "ಮುನ್ಸೂಚನೆಯ ವಿಶ್ವಾಸಾರ್ಹತೆಯ ಮೀಟರ್",
        'urban': "ನಗರು",
        'rural': "ಗ್ರಾಮೀಣ",
        'high': "ಹೆಚ್ಚು",
        'medium': "ಮಧ್ಯಮ",
        'low': "ಕಡಿಮೆ",
        'n_a': "ಲಭ್ಯವಿಲ್ಲ",
        'baseline_txt': "ಬೇಸ್‌ಲೈನ್",
        'range_text_fmt': "ಮತದಾನ ಸಂಭವನೀಯತೆಯ ಶ್ರೇಣಿ: {min_val:.2f}% ರಿಂದ {max_val:.2f}%",
        'risk_desc_high': "ಐತಿಹಾಸಿಕ ಮಟ್ಟಕ್ಕೆ ಹೋಲಿಸಿದರೆ ಗಮನಾರ್ಹ ಭಾಗವಹಿಸುವಿಕೆ ಕುಸಿತವನ್ನು ನಿರೀಕ್ಷಿಸಲಾಗಿದೆ. ತಕ್ಷಣದ ನಾಗರಿಕ ಸಂಪರ್ಕ ಅಗತ್ಯವಿದೆ.",
        'risk_desc_medium': "ಮತದಾನದಲ್ಲಿ ಸೌಮ್ಯ ಕೊರತೆ ಮುನ್ಸೂಚಿಸಲಾಗಿದೆ. ಮತದಾನದ ವೇಗವನ್ನು ನಿಕಟವಾಗಿ ಮೇಲ್ವಿಚಾರಣೆ ಮಾಡಿ.",
        'risk_desc_low': "ಮತದಾರರ ಭಾಗವಹಿಸುವಿಕೆಯು ಬಲವಾಗಿ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ ಅಥವಾ ಐತಿಹಾಸಿಕ ಸರಾಸರಿಗಿಂತ ಹೆಚ್ಚಾಗಿದೆ."
    }
}

def get_layout(lang='en'):
    t = PAGE_TRANSLATIONS.get(lang, PAGE_TRANSLATIONS['en'])
    states = data_service.get_states()
    state_options = [{'label': s, 'value': s} for s in states]
    
    # Left Column: Inputs Form
    inputs_card = dbc.Card([
        html.H5(t['params_header'], className="mb-4", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
        
        # Preset loading option
        dbc.Row([
            dbc.Col([
                html.Label(t['preset_state'], className="form-label-custom"),
                dcc.Dropdown(
                    id='pred-state-select',
                    options=state_options,
                    value=states[0] if states else None,
                    clearable=False,
                    className="bg-dark text-white border-secondary mb-3"
                )
            ], md=6),
            dbc.Col([
                html.Label(t['preset_district'], className="form-label-custom"),
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
                html.Label(t['hist_turnout'], className="form-label-custom"),
                dbc.Input(id='pred-hist-turnout', type='number', min=30, max=100, step=0.1, value=68.5, className="bg-dark text-white border-secondary mb-3")
            ], md=6),
            dbc.Col([
                html.Label(t['literacy'], className="form-label-custom"),
                dbc.Input(id='pred-literacy', type='number', min=30, max=100, step=0.1, value=75.2, className="bg-dark text-white border-secondary mb-3")
            ], md=6),
        ]),
        
        dbc.Row([
            dbc.Col([
                html.Label(t['region_type'], className="form-label-custom"),
                dcc.Dropdown(
                    id='pred-region-type',
                    options=[{'label': t['urban'], 'value': 'Urban'}, {'label': t['rural'], 'value': 'Rural'}],
                    value='Rural',
                    clearable=False,
                    className="bg-dark text-white border-secondary mb-3"
                )
            ], md=6),
            dbc.Col([
                html.Label(t['holiday'], className="form-label-custom"),
                dcc.Dropdown(
                    id='pred-holiday',
                    options=[{'label': t['holiday_yes'], 'value': 1}, {'label': t['holiday_no'], 'value': 0}],
                    value=0,
                    clearable=False,
                    className="bg-dark text-white border-secondary mb-3"
                )
            ], md=6),
        ]),
        
        # Sliders for parameters
        html.Div([
            html.Label(t['awareness'], className="form-label-custom"),
            dcc.Slider(0, 100, 1, value=65, id='pred-awareness', className="mb-4")
        ]),
        
        html.Div([
            html.Label(t['accessibility'], className="form-label-custom"),
            dcc.Slider(0, 100, 1, value=70, id='pred-accessibility', className="mb-4")
        ]),
        
        html.Div([
            html.Label(t['weather'], className="form-label-custom"),
            dcc.Slider(0, 100, 1, value=75, id='pred-weather', className="mb-4")
        ]),
        
        html.Div([
            html.Label(t['campaign'], className="form-label-custom"),
            dcc.Slider(0, 100, 1, value=60, id='pred-campaign', className="mb-4")
        ]),
        
        dbc.Button(t['btn_forecast'], id='predict-btn', color="primary", className="w-100 mt-2", style={'fontWeight': '600'})
    ], className="stat-card p-4 overflow-visible")

    # Right Column: Output Results View
    outputs_panel = html.Div([
        # Prediction Output card
        dbc.Card([
            html.H5(t['results_header'], className="mb-4", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
            
            dbc.Row([
                dbc.Col([
                    html.Div(t['expected_turnout'], style={'fontSize': '0.9rem', 'color': '#94A3B8'}),
                    html.Div(id='pred-out-turnout', style={'fontSize': '3.2rem', 'fontWeight': 'bold', 'color': '#60A5FA', 'fontFamily': 'Poppins'}),
                    html.Div(id='pred-out-range', className="text-muted", style={'fontSize': '0.8rem', 'marginTop': '-5px'})
                ], md=6, className="text-center border-end border-secondary mb-3"),
                
                dbc.Col([
                    html.Div(t['risk_alert'], style={'fontSize': '0.9rem', 'color': '#94A3B8'}),
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
            html.H5(t['xai_header'], className="mb-3", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
            html.P(t['xai_desc'], style={'fontSize': '0.8rem', 'color': '#94A3B8', 'marginBottom': '1rem'}),
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
            html.H3(t['title'], style={'fontFamily': 'Poppins', 'fontWeight': '600', 'color': '#F8FAFC'}),
            html.P(t['subtitle'], style={'color': '#94A3B8'})
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
    State('pred-holiday', 'value'),
    State('lang-store', 'data')
)
def execute_prediction(n_clicks, hist, literacy, region_type, awareness, accessibility, weather, campaign, holiday, lang):
    if not lang:
        lang = 'en'
    t = PAGE_TRANSLATIONS.get(lang, PAGE_TRANSLATIONS['en'])
    
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
    range_text = t['range_text_fmt'].format(min_val=(pred_turnout - mae), max_val=(pred_turnout + mae))
    
    # 2. Risk Alert color formatting
    t_risk_label = t[risk_label.lower()]
    if risk_label == 'High':
        risk_color = {'color': '#EF4444'}
        risk_desc = t['risk_desc_high']
    elif risk_label == 'Medium':
        risk_color = {'color': '#FACC15'}
        risk_desc = t['risk_desc_medium']
    else:
        risk_color = {'color': '#22C55E'}
        risk_desc = t['risk_desc_low']
        
    # 3. Plotly Gauge for Confidence Indicator
    confidence_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=confidence,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': t['gauge_title'], 'font': {'color': '#94A3B8', 'size': 12, 'family': 'Poppins'}},
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
    
    clean_features = {
        'Historical Regional Baseline': {'en': 'Historical Regional Baseline', 'hi': 'ऐतिहासिक क्षेत्रीय आधारभूत रेखा', 'kn': 'ಐತಿಹಾಸಿಕ ಪ್ರಾದೇಶಿಕ ಬೇಸ್‌ಲೈನ್'},
        'Literacy Level Deviation': {'en': 'Literacy Level Deviation', 'hi': 'साक्षरता स्तर विचलन', 'kn': 'ಸಾಕ್ಷರತಾ ಮಟ್ಟದ ವಿಚಲನ'},
        'Awareness Campaign Impact': {'en': 'Awareness Campaign Impact', 'hi': 'जागरूकता अभियान प्रभाव', 'kn': 'ಜಾಗೃತಿ ಅಭಿಯಾನದ ಪ್ರಭಾವ'},
        'Booth Access Infrastructure': {'en': 'Booth Access Infrastructure', 'hi': 'मतदान केंद्र पहुंच बुनियादी ढांचा', 'kn': 'ಮತಗಟ್ಟೆ ಪ್ರವೇಶ ಮೂಲಸೌಕರ್ಯ'},
        'Weather Comfort Index': {'en': 'Weather Comfort Index', 'hi': 'मौसम आराम सूचकांक', 'kn': 'ಹವಾಮಾನ ಕಂಫರ್ಟ್ ಸೂಚ್ಯಂಕ'},
        'Political Campaign Density': {'en': 'Political Campaign Density', 'hi': 'राजनीतिक अभियान घनत्व', 'kn': 'ರಾಜಕೀಯ ಪ್ರಚಾರದ ಸಾಂದ್ರತೆ'},
        'Holiday Drag Factor': {'en': 'Holiday Drag Factor', 'hi': 'छुट्टी का खिंचाव कारक', 'kn': 'ರಜಾದಿನದ ಡ್ರ್ಯಾಗ್ ಅಂಶ'},
        'Urban/Rural Density Delta': {'en': 'Urban/Rural Density Delta', 'hi': 'शहरी/ग्रामीण घनत्व डेल्टा', 'kn': 'ನಗರು/ಗ್ರಾಮೀಣ ಸಾಂದ್ರತೆಯ ಡೆಲ್ಟಾ'},
        'Interactive Model Adjustments': {'en': 'Interactive Model Adjustments', 'hi': 'इंटरएक्टिव मॉडल समायोजन', 'kn': 'ಸಂವಾದಾತ್ಮಕ ಮಾದರಿ ಹೊಂದಾಣಿಕೆಗಳು'}
    }

    for d in drivers:
        val = d['contribution']
        feature_name = d['feature']
        t_feat = clean_features.get(feature_name, {}).get(lang, feature_name)
        
        if d['type'] == 'baseline':
            badge = html.Span(f"{val:.2f}% {t['baseline_txt']}", className="badge bg-primary ms-auto", style={'fontWeight': 'bold', 'fontSize': '0.75rem'})
        else:
            if val > 0:
                badge = html.Span(f"+{val:.2f}%", className="badge bg-success text-white ms-auto", style={'fontWeight': 'bold', 'fontSize': '0.75rem', 'backgroundColor': 'rgba(34, 197, 94, 0.2) !important'})
            elif val < 0:
                badge = html.Span(f"{val:.2f}%", className="badge bg-danger text-white ms-auto", style={'fontWeight': 'bold', 'fontSize': '0.75rem', 'backgroundColor': 'rgba(239, 68, 68, 0.2) !important'})
            else:
                badge = html.Span("0.00%", className="badge bg-secondary ms-auto", style={'fontSize': '0.75rem'})
                
        xai_elements.append(
            html.Div([
                html.Span(t_feat, style={'fontSize': '0.85rem', 'color': '#F8FAFC'}),
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
        clean_features_importance = {
            'historical_turnout': {'en': 'Historical Turnout', 'hi': 'ऐतिहासिक मतदान', 'kn': 'ಐತಿಹಾಸಿಕ ಮತದಾನ'},
            'literacy_rate': {'en': 'Literacy Rate', 'hi': 'साक्षरता दर', 'kn': 'ಸಾಕ್ಷರತಾ ಪ್ರಮಾಣ'},
            'awareness_score': {'en': 'Awareness Score', 'hi': 'जागरूकता स्कोर', 'kn': 'ಜಾಗೃತಿ ಸ್ಕೋರ್'},
            'transport_accessibility': {'en': 'Booth Access Score', 'hi': 'बूथ पहुंच स्कोर', 'kn': 'ಮತಗಟ್ಟೆ ಪ್ರವೇಶ ಸ್ಕೋರ್'},
            'weather_score': {'en': 'Weather comfort', 'hi': 'मौसम आराम', 'kn': 'ಹವಾಮಾನ ಕಂಫರ್ಟ್'},
            'campaign_intensity': {'en': 'Campaign Budget', 'hi': 'अभियान बजट', 'kn': 'ಪ್ರಚಾರ ಬಜೆಟ್'},
            'holiday_factor': {'en': 'Holiday Proximity', 'hi': 'छुट्टी की निकटता', 'kn': 'ರಜಾದಿನದ ಸಾಮೀಪ್ಯ'},
            'is_urban': {'en': 'Urban Status', 'hi': 'शहरी स्थिति', 'kn': 'ನಗರದ ಸ್ಥಿತಿ'}
        }
        labels = [clean_features_importance.get(f, {}).get(lang, f) for f in features]
        
        # Sort together
        sorted_pairs = sorted(zip(values, labels))
        values, labels = zip(*sorted_pairs)
    else:
        # Fallback values
        fallback_labels = {
            'Holiday Proximity': {'en': 'Holiday Proximity', 'hi': 'छुट्टी की निकटता', 'kn': 'ರಜಾದಿನದ ಸಾಮೀಪ್ಯ'},
            'Urban Status': {'en': 'Urban Status', 'hi': 'शहरी स्थिति', 'kn': 'ನಗರದ ಸ್ಥಿತಿ'},
            'Weather comfort': {'en': 'Weather comfort', 'hi': 'मौसम आराम', 'kn': 'ಹವಾಮಾನ ಕಂಫರ್ಟ್'},
            'Booth Access Score': {'en': 'Booth Access Score', 'hi': 'बूथ पहुंच स्कोर', 'kn': 'ಮತಗಟ್ಟೆ ಪ್ರವೇಶ ಸ್ಕೋರ್'},
            'Campaign Budget': {'en': 'Campaign Budget', 'hi': 'अभियान बजट', 'kn': 'ಪ್ರಚಾರ ಬಜೆಟ್'},
            'Awareness Score': {'en': 'Awareness Score', 'hi': 'जागरूकता स्कोर', 'kn': 'ಜಾಗೃತಿ ಸ್ಕೋರ್'},
            'Literacy Rate': {'en': 'Literacy Rate', 'hi': 'साक्षरता दर', 'kn': 'ಸಾಕ್ಷರತಾ ಪ್ರಮಾಣ'},
            'Historical Turnout': {'en': 'Historical Turnout', 'hi': 'ऐतिहासिक मतदान', 'kn': 'ಐತಿಹಾಸಿಕ ಮತದಾನ'}
        }
        labels = [fallback_labels[f][lang] for f in ['Holiday Proximity', 'Urban Status', 'Weather comfort', 'Booth Access Score', 'Campaign Budget', 'Awareness Score', 'Literacy Rate', 'Historical Turnout']]
        values = [0.03, 0.05, 0.08, 0.12, 0.15, 0.17, 0.18, 0.22]
        
    importance_fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation='h',
        marker_color='#2563EB'
    ))
    importance_fig.update_layout(
        title=dict(text=t['chart_importance'], font=dict(color='#F8FAFC', family='Poppins')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        xaxis=dict(gridcolor='#1E293B', title=t['influence_weight']),
        yaxis=dict(gridcolor='#1E293B'),
        margin=dict(l=140, r=20, t=40, b=40)
    )
    
    return turnout_text, range_text, t_risk_label, risk_color, risk_desc, confidence_fig, xai_list, importance_fig
