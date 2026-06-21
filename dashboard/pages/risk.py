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
        'title': "AI Risk Intelligence Center",
        'subtitle': "Monitor real-time participation risk indices, investigate underperforming voting corridors, and prioritize awareness efforts.",
        'filter_state': "Inspect State",
        'filter_category': "Priority Category",
        'all_states': "All States",
        'all_categories': "All Risk Categories",
        'cat_slowdown': "Turnout Slowdown (Deficit > 3%)",
        'cat_awareness': "Awareness Deficit (Awareness < 60)",
        'cat_infrastructure': "Infrastructure / Access Gaps",
        'cat_weather': "Severe Weather Gaps",
        'search_placeholder': "Type constituency name...",
        'search_lbl': "Search Risk Zones",
        'summary_header': "Active Risk Summary",
        'metrics_high': "HIGH RISK ZONES",
        'metrics_med': "MEDIUM RISK ZONES",
        'metrics_deficit': "AVERAGE PARTICIPATION DEFICIT",
        'metrics_below': "below baseline",
        'metrics_compared': "Compared to historical averages",
        'correlation_header': "PRIMARY TRIGGER CORRELATION",
        'corr_weather': "Weather impact present in {count} areas.",
        'corr_awareness': "Awareness deficits found in {count} areas.",
        'corr_accessibility': "Accessibility barriers found in {count} areas.",
        'chart_title': "Top Turnout Deficits (Baseline vs Live)",
        'chart_y_title': "Deficit Percentage (Lower is Better)",
        'chart_no_data': "No at-risk zones match current filters",
        'log_header': "Critical Risk Operations Log",
        'no_active_zones': "No active risk zones identified for current criteria.",
        'tbl_constituency': "Constituency",
        'tbl_district': "District",
        'tbl_state': "State",
        'tbl_current': "Current Turnout",
        'tbl_historical': "Historical Turnout",
        'tbl_deviation': "Turnout Deviation",
        'tbl_risk': "Risk Classification",
        'tbl_triggers': "Primary Triggers",
        'trigger_weather': "Weather",
        'trigger_awareness': "Awareness Gaps",
        'trigger_transport': "Transport Gaps",
        'trigger_apathy': "Apathy",
        'low': "Low",
        'medium': "Medium",
        'high': "High",
        'no_data': "No data"
    },
    'hi': {
        'title': "एआई जोखिम इंटेलिजेंस सेंटर",
        'subtitle': "वास्तविक समय भागीदारी जोखिम सूचकांकों की निगरानी करें, कम प्रदर्शन करने वाले मतदान गलियारों की जांच करें और जागरूकता प्रयासों को प्राथमिकता दें।",
        'filter_state': "राज्य का निरीक्षण करें",
        'filter_category': "प्राथमिकता श्रेणी",
        'all_states': "सभी राज्य",
        'all_categories': "सभी जोखिम श्रेणियां",
        'cat_slowdown': "मतदान में गिरावट (घाटा > 3%)",
        'cat_awareness': "जागरूकता घाटा (जागरूकता < 60)",
        'cat_infrastructure': "बुनियादी ढांचा / पहुंच अंतराल",
        'cat_weather': "गंभीर मौसम अंतराल",
        'search_placeholder': "निर्वाचन क्षेत्र का नाम टाइप करें...",
        'search_lbl': "जोखिम क्षेत्र खोजें",
        'summary_header': "सक्रिय जोखिम सारांश",
        'metrics_high': "उच्च जोखिम क्षेत्र",
        'metrics_med': "मध्यम जोखिम क्षेत्र",
        'metrics_deficit': "औसत भागीदारी घाटा",
        'metrics_below': "आधारभूत रेखा से नीचे",
        'metrics_compared': "ऐतिहासिक औसत की तुलना में",
        'correlation_header': "प्राथमिक ट्रिगर सहसंबंध",
        'corr_weather': "{count} क्षेत्रों में मौसम का प्रभाव मौजूद है।",
        'corr_awareness': "{count} क्षेत्रों में जागरूकता की कमी पाई गई।",
        'corr_accessibility': "{count} क्षेत्रों में पहुंच संबंधी बाधाएं पाई गईं।",
        'chart_title': "शीर्ष मतदान घाटे (आधारभूत बनाम लाइव)",
        'chart_y_title': "घाटा प्रतिशत (कम बेहतर है)",
        'chart_no_data': "कोई भी जोखिम क्षेत्र वर्तमान फिल्टर से मेल नहीं खाता है",
        'log_header': "महत्वपूर्ण जोखिम संचालन लॉग",
        'no_active_zones': "वर्तमान मानदंडों के लिए कोई सक्रिय जोखिम क्षेत्र नहीं पहचाना गया।",
        'tbl_constituency': "निर्वाचन क्षेत्र",
        'tbl_district': "जिला",
        'tbl_state': "राज्य",
        'tbl_current': "वर्तमान मतदान",
        'tbl_historical': "ऐतिहासिक मतदान",
        'tbl_deviation': "मतदान विचलन",
        'tbl_risk': "जोखिम वर्गीकरण",
        'tbl_triggers': "प्राथमिक ट्रिगर",
        'trigger_weather': "मौसम",
        'trigger_awareness': "जागरूकता अंतर",
        'trigger_transport': "परिवहन अंतर",
        'trigger_apathy': "उदासीनता",
        'low': "निम्न",
        'medium': "मध्यम",
        'high': "उच्च",
        'no_data': "कोई डेटा नहीं"
    },
    'kn': {
        'title': "ಎಐ ಅಪಾಯ ವಿಶ್ಲೇಷಣಾ ಕೇಂದ್ರ",
        'subtitle': "ನೈಜ-ಸಮಯದ ಭಾಗವಹಿಸುವಿಕೆ ಅಪಾಯದ ಸೂಚ್ಯಂಕಗಳನ್ನು ಮೇಲ್ವಿಚಾರಣೆ ಮಾಡಿ, ಕಡಿಮೆ ಮತದಾನದ ಕಾರಿಡಾರ್‌ಗಳನ್ನು ತನಿಖೆ ಮಾಡಿ ಮತ್ತು ಜಾಗೃತಿ ಪ್ರಯತ್ನಗಳಿಗೆ ಆದ್ಯತೆ ನೀಡಿ.",
        'filter_state': "ರಾಜ್ಯವನ್ನು ಪರಿಶೀಲಿಸಿ",
        'filter_category': "ಆದ್ಯತೆಯ ವರ್ಗ",
        'all_states': "ಎಲ್ಲಾ ರಾಜ್ಯಗಳು",
        'all_categories': "ಎಲ್ಲಾ ಅಪಾಯದ ವರ್ಗಗಳು",
        'cat_slowdown': "ಮತದಾನ ಕುಸಿತ (ಕೊರತೆ > 3%)",
        'cat_awareness': "ಜಾಗೃತಿಯ ಕೊರತೆ (ಜಾಗೃತಿ < 60)",
        'cat_infrastructure': "ಮೂಲಸೌಕರ್ಯ / ಪ್ರವೇಶದ ಅಂತರ",
        'cat_weather': "ವಿಪರೀತ ಹವಾಮಾನದ ಕೊರತೆ",
        'search_placeholder': "ಮತಕ್ಷೇತ್ರದ ಹೆಸರನ್ನು ಟೈಪ್ ಮಾಡಿ...",
        'search_lbl': "ಅಪಾಯದ ವಲಯಗಳನ್ನು ಹುಡುಕಿ",
        'summary_header': "ಸಕ್ರಿಯ ಅಪಾಯದ ಸಾರಾಂಶ",
        'metrics_high': "ಹೆಚ್ಚಿನ ಅಪಾಯದ ವಲಯಗಳು",
        'metrics_med': "ಮಧ್ಯಮ ಅಪಾಯದ ವಲಯಗಳು",
        'metrics_deficit': "ಸರಾಸರಿ ಭಾಗವಹಿಸುವಿಕೆಯ ಕೊರತೆ",
        'metrics_below': "ಬೇಸ್‌ಲೈನ್‌ಗಿಂತ ಕಡಿಮೆ",
        'metrics_compared': "ಐತಿಹಾಸಿಕ ಸರಾಸರಿಗಳಿಗೆ ಹೋಲಿಸಿದರೆ",
        'correlation_header': "ಪ್ರಾಥಮಿಕ ಪ್ರಚೋದಕ ಸಂಬಂಧ",
        'corr_weather': "{count} ಪ್ರದೇಶಗಳಲ್ಲಿ ಹವಾಮಾನದ ಪ್ರಭಾವ ಕಂಡುಬಂದಿದೆ.",
        'corr_awareness': "{count} ಪ್ರದೇಶಗಳಲ್ಲಿ ಜಾಗೃತಿಯ ಕೊರತೆ ಕಂಡುಬಂದಿದೆ.",
        'corr_accessibility': "{count} ಪ್ರದೇಶಗಳಲ್ಲಿ ಪ್ರವೇಶದ ಅಡಚಣೆಗಳು ಕಂಡುಬಂದಿವೆ.",
        'chart_title': "ಉನ್ನತ ಮತದಾನದ ಕೊರತೆಗಳು (ಬೇಸ್‌ಲೈನ್ ವಿರುದ್ಧ ಲೈವ್)",
        'chart_y_title': "ಕೊರತೆಯ ಪ್ರಮಾಣ (ಕಡಿಮೆ ಇದ್ದಷ್ಟೂ ಉತ್ತಮ)",
        'chart_no_data': "ಯಾವುದೇ ಅಪಾಯದ ವಲಯಗಳು ಪ್ರಸ್ತುತ ಫಿಲ್ಟರ್‌ಗಳಿಗೆ ಹೊಂದಿಕೆಯಾಗುತ್ತಿಲ್ಲ",
        'log_header': "ನಿರ್ಣಾಯಕ ಅಪಾಯ ಕಾರ್ಯಾಚರಣೆಗಳ ಲಾಗ್",
        'no_active_zones': "ಪ್ರಸ್ತುತ ಮಾನದಂಡಗಳಿಗೆ ಯಾವುದೇ ಸಕ್ರಿಯ ಅಪಾಯದ ವಲಯಗಳು ಕಂಡುಬಂದಿಲ್ಲ.",
        'tbl_constituency': "ಮತಕ್ಷೇತ್ರ",
        'tbl_district': "ಜಿಲ್ಲೆ",
        'tbl_state': "ರಾಜ್ಯ",
        'tbl_current': "ಪ್ರಸ್ತುತ ಮತದಾನ",
        'tbl_historical': "ಐತಿಹಾಸಿಕ ಮತದಾನ",
        'tbl_deviation': "ಮತದಾನದ ವಿಚಲನ",
        'tbl_risk': "ಅಪಾಯದ ವರ್ಗೀಕರಣ",
        'tbl_triggers': "ಪ್ರಾಥಮಿಕ ಪ್ರಚೋದಕಗಳು",
        'trigger_weather': "ಹವಾಮಾನ",
        'trigger_awareness': "ಜಾಗೃತಿಯ ಕೊರತೆ",
        'trigger_transport': "ಸಾರಿಗೆ ಕೊರತೆ",
        'trigger_apathy': "ಉದಾಸೀನತೆ",
        'low': "ಕಡಿಮೆ",
        'medium': "ಮಧ್ಯಮ",
        'high': "ಹೆಚ್ಚು",
        'no_data': "ಡೇಟಾ ಇಲ್ಲ"
    }
}

def get_layout(lang='en'):
    t = PAGE_TRANSLATIONS.get(lang, PAGE_TRANSLATIONS['en'])
    states = data_service.get_states()
    state_options = [{'label': t['all_states'], 'value': 'ALL'}] + [{'label': s, 'value': s} for s in states]
    
    # Grid Layout
    return html.Div([
        # Header Row
        html.Div([
            html.H3(t['title'], style={'fontFamily': 'Poppins', 'fontWeight': '600', 'color': '#F8FAFC'}),
            html.P(t['subtitle'], style={'color': '#94A3B8'})
        ], className="mb-4"),
        
        # Risk Filters
        dbc.Card([
            dbc.Row([
                dbc.Col([
                    html.Label(t['filter_state'], className="form-label-custom"),
                    dcc.Dropdown(
                        id='risk-state-filter',
                        options=state_options,
                        value='ALL',
                        clearable=False,
                        className="bg-dark text-white border-secondary"
                    )
                ], md=4, xs=12),
                
                dbc.Col([
                    html.Label(t['filter_category'], className="form-label-custom"),
                    dcc.Dropdown(
                        id='risk-category-filter',
                        options=[
                            {'label': t['all_categories'], 'value': 'ALL'},
                            {'label': t['cat_slowdown'], 'value': 'slowdown'},
                            {'label': t['cat_awareness'], 'value': 'awareness'},
                            {'label': t['cat_infrastructure'], 'value': 'infrastructure'},
                            {'label': t['cat_weather'], 'value': 'weather'}
                        ],
                        value='ALL',
                        clearable=False,
                        className="bg-dark text-white border-secondary"
                    )
                ], md=4, xs=12),
                
                dbc.Col([
                    html.Label(t['search_lbl'], className="form-label-custom"),
                    dbc.Input(
                        id='risk-search-input',
                        placeholder=t['search_placeholder'],
                        type="text",
                        className="bg-dark text-white border-secondary"
                    )
                ], md=4, xs=12),
            ], className="g-3")
        ], className="stat-card mb-4 overflow-visible", style={'padding': '1.2rem'}),
        
        # Risk analytics cards
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(id='risk-zones-chart', config={'displayModeBar': False})
                ], className="stat-card mb-4")
            ], xl=8, lg=7, md=12),
            
            dbc.Col([
                dbc.Card([
                    html.H5(t['summary_header'], className="mb-4", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
                    html.Div(id='risk-metrics-panel')
                ], className="stat-card mb-4", style={'height': 'calc(100% - 1.5rem)'})
            ], xl=4, lg=5, md=12)
        ]),
        
        # Risk Table Grid
        html.H5(t['log_header'], className="mb-3", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
        dbc.Card([
            html.Div(id='risk-log-table')
        ], className="stat-card", style={'padding': '0'})
    ])

@callback(
    Output('risk-zones-chart', 'figure'),
    Output('risk-metrics-panel', 'children'),
    Output('risk-log-table', 'children'),
    Input('risk-state-filter', 'value'),
    Input('risk-category-filter', 'value'),
    Input('risk-search-input', 'value'),
    State('lang-store', 'data')
)
def update_risk_dashboard(selected_state, selected_category, search_query, lang):
    if not lang:
        lang = 'en'
    t = PAGE_TRANSLATIONS.get(lang, PAGE_TRANSLATIONS['en'])

    # Filter dataset
    df = data_service.df
    if df.empty:
        return go.Figure(), html.Div(t['no_data']), html.Div(t['no_data'])
        
    filtered = df.copy()
    if selected_state and selected_state != 'ALL':
        filtered = filtered[filtered['state'] == selected_state]
        
    # Apply category logic
    if selected_category == 'slowdown':
        filtered = filtered[(filtered['historical_turnout'] - filtered['current_turnout']) > 3.0]
    elif selected_category == 'awareness':
        filtered = filtered[filtered['awareness_score'] < 60]
    elif selected_category == 'infrastructure':
        filtered = filtered[filtered['transport_accessibility'] < 60]
    elif selected_category == 'weather':
        filtered = filtered[filtered['weather_score'] < 50]
        
    if search_query:
        q = search_query.lower()
        filtered = filtered[filtered['constituency'].str.lower().str.contains(q)]
        
    # Sorted by deficit descending
    filtered['turnout_deficit'] = filtered['historical_turnout'] - filtered['current_turnout']
    filtered = filtered.sort_values(by='turnout_deficit', ascending=False)
    
    # 1. Summary Metrics
    total_high = (filtered['risk_level'] == 'High').sum()
    total_med = (filtered['risk_level'] == 'Medium').sum()
    avg_deficit = filtered['turnout_deficit'].mean() if not filtered.empty else 0.0
    
    metrics_layout = html.Div([
        dbc.Row([
            dbc.Col([
                html.Div(t['metrics_high'], style={'fontSize': '0.75rem', 'color': '#94A3B8'}),
                html.Div(f"{total_high}", style={'fontSize': '1.8rem', 'fontWeight': 'bold', 'color': '#EF4444'})
            ], xs=6),
            dbc.Col([
                html.Div(t['metrics_med'], style={'fontSize': '0.75rem', 'color': '#94A3B8'}),
                html.Div(f"{total_med}", style={'fontSize': '1.8rem', 'fontWeight': 'bold', 'color': '#FACC15'})
            ], xs=6)
        ], className="g-0 mb-4"),
        
        html.Div([
            html.Div(t['metrics_deficit'], style={'fontSize': '0.75rem', 'color': '#94A3B8'}),
            html.Div(f"{avg_deficit:.2f}% {t['metrics_below']}", style={'fontSize': '1.2rem', 'fontWeight': '600', 'color': '#F8FAFC'}),
            html.Div(t['metrics_compared'], style={'fontSize': '0.7rem', 'color': '#94A3B8'})
        ], className="mb-4"),
        
        html.Div([
            html.Div(t['correlation_header'], style={'fontSize': '0.75rem', 'color': '#94A3B8'}),
            html.Ul([
                html.Li(t['corr_weather'].format(count=int((filtered['weather_score'] < 50).sum())), style={'fontSize': '0.8rem', 'color': '#F8FAFC', 'marginBottom': '0.3rem'}),
                html.Li(t['corr_awareness'].format(count=int((filtered['awareness_score'] < 60).sum())), style={'fontSize': '0.8rem', 'color': '#F8FAFC', 'marginBottom': '0.3rem'}),
                html.Li(t['corr_accessibility'].format(count=int((filtered['transport_accessibility'] < 60).sum())), style={'fontSize': '0.8rem', 'color': '#F8FAFC'})
            ], className="ps-3 mt-1")
        ])
    ])
    
    # 2. Risk Zones Chart (Top 12 underperforming zones)
    chart_df = filtered.head(12)
    chart_fig = go.Figure()
    
    if chart_df.empty:
        chart_fig.update_layout(
            title=t['chart_no_data'],
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94A3B8')
        )
    else:
        chart_fig.add_trace(go.Bar(
            x=chart_df['constituency'],
            y=chart_df['turnout_deficit'],
            marker_color='#EF4444',
            name=t['tbl_deviation']
        ))
        chart_fig.update_layout(
            title=dict(text=t['chart_title'], font=dict(color='#F8FAFC', family='Poppins')),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94A3B8'),
            xaxis=dict(gridcolor='#1E293B', tickangle=45),
            yaxis=dict(gridcolor='#1E293B', title=t['chart_y_title']),
            margin=dict(l=40, r=20, t=40, b=80)
        )
        
    # 3. Log Table
    table_rows = []
    if filtered.empty:
        table_rows.append(html.Tr([html.Td(t['no_active_zones'], colSpan=8, className="text-center text-muted")]))
    else:
        # Display top 15 risk rows in table
        for idx, row in filtered.head(15).iterrows():
            deficit_val = row['turnout_deficit']
            deficit_color = '#EF4444' if deficit_val > 3.0 else '#FACC15'
            
            t_risk_label = t[row['risk_level'].lower()]
            risk_badge = html.Span(t_risk_label, className=f"badge bg-{'danger' if row['risk_level'] == 'High' else 'warning'}")
            
            # Diagnose primary trigger
            triggers = []
            if row['weather_score'] < 50:
                triggers.append(t['trigger_weather'])
            if row['awareness_score'] < 60:
                triggers.append(t['trigger_awareness'])
            if row['transport_accessibility'] < 60:
                triggers.append(t['trigger_transport'])
            if not triggers:
                triggers.append(t['trigger_apathy'])
                
            trigger_text = ", ".join(triggers)
            
            table_rows.append(html.Tr([
                html.Td(row['constituency'], style={'fontWeight': '600'}),
                html.Td(row['district']),
                html.Td(row['state']),
                html.Td(f"{row['current_turnout']}%"),
                html.Td(f"{row['historical_turnout']}%"),
                html.Td(f"+{deficit_val:.2f}%" if deficit_val < 0 else f"-{deficit_val:.2f}%", style={'color': deficit_color, 'fontWeight': 'bold'}),
                html.Td(risk_badge),
                html.Td(trigger_text, style={'fontStyle': 'italic', 'color': '#94A3B8'})
            ]))
            
    log_table = dbc.Table([
        html.Thead(html.Tr([
            html.Th(t['tbl_constituency']), html.Th(t['tbl_district']), html.Th(t['tbl_state']), 
            html.Th(t['tbl_current']), html.Th(t['tbl_historical']), html.Th(t['tbl_deviation']),
            html.Th(t['tbl_risk']), html.Th(t['tbl_triggers'])
        ]))] + [html.Tbody(table_rows)],
        className="table-custom",
        bordered=False,
        hover=True,
        responsive=True
    )
    
    return chart_fig, metrics_layout, log_table
