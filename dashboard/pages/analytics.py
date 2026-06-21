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
        'title': 'State & District Drill-Down Analytics',
        'desc': 'Explore voter engagement, compare region rankings, and view booth level participation alerts.',
        'filter_state': 'Filter State',
        'filter_district': 'Filter District',
        'risk_level': 'Risk Level',
        'region_type': 'Region Type',
        'search_const': 'Search Constituency',
        'cell_title': 'Constituency Intelligence Cells',
        'all_states': 'All States',
        'all_districts': 'All Districts',
        'all_risks': 'All Risk Levels',
        'all_types': 'All Types',
        'search_placeholder': 'Type to search...',
        'chart_title_perf': 'Top Constituency Performance vs Historical Baseline',
        'chart_title_mom': 'Participation Momentum Distribution',
        'no_records': 'No records found matching current criteria.',
        'predicted_turnout': 'Predicted Turnout',
        'historical_turnout': 'Historical Turnout',
        'turnout_lbl': 'Turnout',
        'historical_lbl': 'Historical',
        'risk_badge': 'Risk',
        'momentum_badge': 'Momentum',
        'more_const': '...and {count} more constituencies. Refine filters to narrow search.',
        'Urban': 'Urban',
        'Rural': 'Rural',
        'Accelerating': 'Accelerating',
        'Stable': 'Stable',
        'Declining': 'Declining',
        'High': 'High',
        'Medium': 'Medium',
        'Low': 'Low'
    },
    'hi': {
        'title': 'राज्य और जिला ड्रिल-डाउन विश्लेषण',
        'desc': 'मतदाता भागीदारी का पता लगाएं, क्षेत्रीय रैंकिंग की तुलना करें और बूथ स्तर की भागीदारी अलर्ट देखें।',
        'filter_state': 'राज्य फ़िल्टर',
        'filter_district': 'जिला फ़िल्टर',
        'risk_level': 'जोखिम स्तर',
        'region_type': 'क्षेत्र प्रकार',
        'search_const': 'निर्वाचन क्षेत्र खोजें',
        'cell_title': 'निर्वाचन क्षेत्र खुफिया सेल',
        'all_states': 'सभी राज्य',
        'all_districts': 'सभी जिले',
        'all_risks': 'सभी जोखिम स्तर',
        'all_types': 'सभी प्रकार',
        'search_placeholder': 'खोजने के लिए टाइप करें...',
        'chart_title_perf': 'ऐतिहासिक आधार रेखा बनाम शीर्ष निर्वाचन क्षेत्र का प्रदर्शन',
        'chart_title_mom': 'भागीदारी गति वितरण',
        'no_records': 'वर्तमान मापदंडों से मेल खाता कोई रिकॉर्ड नहीं मिला।',
        'predicted_turnout': 'पूर्वानुमानित मतदान',
        'historical_turnout': 'ऐतिहासिक मतदान',
        'turnout_lbl': 'मतदान',
        'historical_lbl': 'ऐतिहासिक',
        'risk_badge': 'जोखिम',
        'momentum_badge': 'गति',
        'more_const': '...और {count} अधिक निर्वाचन क्षेत्र। खोज को सीमित करने के लिए फ़िल्टर परिशोधित करें।',
        'Urban': 'शहरी',
        'Rural': 'ग्रामीण',
        'Accelerating': 'तेज',
        'Stable': 'स्थिर',
        'Declining': 'गिरावट',
        'High': 'उच्च',
        'Medium': 'मध्यम',
        'Low': 'कम'
    },
    'kn': {
        'title': 'ರಾಜ್ಯ ಮತ್ತು ಜಿಲ್ಲಾವಾರು ವಿಶ್ಲೇಷಣೆ',
        'desc': 'ಮತದಾರರ ಭಾಗವಹಿಸುವಿಕೆಯನ್ನು ಅನ್ವೇಷಿಸಿ, ಪ್ರಾದೇಶಿಕ ಶ್ರೇಯಾಂಕಗಳನ್ನು ಹೋಲಿಕೆ ಮಾಡಿ ಮತ್ತು ಮತಗಟ್ಟೆ ಮಟ್ಟದ ಎಚ್ಚರಿಕೆಗಳನ್ನು ವೀಕ್ಷಿಸಿ.',
        'filter_state': 'ರಾಜ್ಯ ಫಿಲ್ಟರ್',
        'filter_district': 'ಜಿಲ್ಲಾ ಫಿಲ್ಟರ್',
        'risk_level': 'ಅಪಾಯದ ಮಟ್ಟ',
        'region_type': 'ಪ್ರದೇಶದ ವಿಧ',
        'search_const': 'ಮತಕ್ಷೇತ್ರ ಹುಡುಕಿ',
        'cell_title': 'ಮತಕ್ಷೇತ್ರದ ಗುಪ್ತಚರ ಸೆಲ್‌ಗಳು',
        'all_states': 'ಎಲ್ಲಾ ರಾಜ್ಯಗಳು',
        'all_districts': 'ಎಲ್ಲಾ ಜಿಲ್ಲೆಗಳು',
        'all_risks': 'ಎಲ್ಲಾ ಅಪಾಯದ ಮಟ್ಟಗಳು',
        'all_types': 'ಎಲ್ಲಾ ವಿಧಗಳು',
        'search_placeholder': 'ಹುಡುಕಲು ಟೈಪ್ ಮಾಡಿ...',
        'chart_title_perf': 'ಐತಿಹಾಸಿಕ ತಳಹದಿ ವಿರುದ್ಧ ಗರಿಷ್ಠ ಮತಕ್ಷೇತ್ರದ ಪ್ರದರ್ಶನ',
        'chart_title_mom': 'ಭಾಗವಹಿಸುವಿಕೆಯ ವೇಗದ ಹಂಚಿಕೆ',
        'no_records': 'ಪ್ರಸ್ತುತ ಮಾನದಂಡಗಳಿಗೆ ಹೊಂದಿಕೆಯಾಗುವ ಯಾವುದೇ ದಾಖಲೆಗಳು ಕಂಡುಬಂದಿಲ್ಲ.',
        'predicted_turnout': 'ಮುನ್ಸೂಚಿತ ಮತದಾನ',
        'historical_turnout': 'ಐತಿಹಾಸಿಕ ಮತದಾನ',
        'turnout_lbl': 'ಮತದಾನ',
        'historical_lbl': 'ಐತಿಹಾಸಿಕ',
        'risk_badge': 'ಅಪಾಯ',
        'momentum_badge': 'ವೇಗ',
        'more_const': '...ಮತ್ತು {count} ಮತಕ್ಷೇತ್ರಗಳು. ಹುಡುಕಾಟವನ್ನು ಕಿರಿದಾಗಿಸಲು ಫಿಲ್ಟರ್‌ಗಳನ್ನು ಪರಿಷ್ಕರಿಸಿ.',
        'Urban': 'ನಗರ',
        'Rural': 'ಗ್ರಾಮೀಣ',
        'Accelerating': 'ವೇಗವರ್ಧನೆ',
        'Stable': 'ಸ್ಥಿರ',
        'Declining': 'ಕುಸಿತ',
        'High': 'ಹೆಚ್ಚು',
        'Medium': 'ಮಧ್ಯಮ',
        'Low': 'ಕಡಿಮೆ'
    }
}

def get_layout(lang='en'):
    states = data_service.get_states()
    t = PAGE_TRANSLATIONS.get(lang, PAGE_TRANSLATIONS['en'])
    
    # State Options
    state_options = [{'label': t['all_states'], 'value': 'ALL'}] + [{'label': s, 'value': s} for s in states]
    
    # Initial layout
    return html.Div([
        # Header Row
        html.Div([
            html.H3(t['title'], style={'fontFamily': 'Poppins', 'fontWeight': '600', 'color': '#F8FAFC'}),
            html.P(t['desc'], style={'color': '#94A3B8'})
        ], className="mb-4"),
        
        # Filtering Controls Card
        dbc.Card([
            dbc.Row([
                dbc.Col([
                    html.Label(t['filter_state'], className="form-label-custom"),
                    dcc.Dropdown(
                        id='state-filter',
                        options=state_options,
                        value='ALL',
                        clearable=False,
                        className="bg-dark text-white border-secondary"
                    )
                ], lg=3, md=6, xs=12, className="mb-2"),
                
                dbc.Col([
                    html.Label(t['filter_district'], className="form-label-custom"),
                    dcc.Dropdown(
                        id='district-filter',
                        options=[{'label': t['all_districts'], 'value': 'ALL'}],
                        value='ALL',
                        clearable=False,
                        className="bg-dark text-white border-secondary"
                    )
                ], lg=3, md=6, xs=12, className="mb-2"),
                
                dbc.Col([
                    html.Label(t['risk_level'], className="form-label-custom"),
                    dcc.Dropdown(
                        id='risk-filter',
                        options=[
                            {'label': t['all_risks'], 'value': 'ALL'},
                            {'label': f"🔴 {t['High']}", 'value': 'High'},
                            {'label': f"🟡 {t['Medium']}", 'value': 'Medium'},
                            {'label': f"🟢 {t['Low']}", 'value': 'Low'}
                        ],
                        value='ALL',
                        clearable=False,
                        className="bg-dark text-white border-secondary"
                    )
                ], lg=2, md=4, xs=6, className="mb-2"),
                
                dbc.Col([
                    html.Label(t['region_type'], className="form-label-custom"),
                    dcc.Dropdown(
                        id='region-type-filter',
                        options=[
                            {'label': t['all_types'], 'value': 'ALL'},
                            {'label': t['Urban'], 'value': 'Urban'},
                            {'label': t['Rural'], 'value': 'Rural'}
                        ],
                        value='ALL',
                        clearable=False,
                        className="bg-dark text-white border-secondary"
                    )
                ], lg=2, md=4, xs=6, className="mb-2"),
                
                dbc.Col([
                    html.Label(t['search_const'], className="form-label-custom"),
                    dbc.Input(
                        id='search-input',
                        placeholder=t['search_placeholder'],
                        type="text",
                        className="bg-dark text-white border-secondary"
                    )
                ], lg=2, md=4, xs=12, className="mb-2"),
            ], className="g-3")
        ], className="stat-card mb-4 overflow-visible", style={'padding': '1.2rem'}),
        
        # Performance Summary row
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(id='ranking-plot', config={'displayModeBar': False, 'responsive': True})
                ], className="stat-card mb-4")
            ], xl=8, lg=7, md=12),
            
            dbc.Col([
                html.Div([
                    dcc.Graph(id='momentum-plot', config={'displayModeBar': False, 'responsive': True})
                ], className="stat-card mb-4")
            ], xl=4, lg=5, md=12)
        ]),
        
        # Grid title and list
        html.H5(t['cell_title'], className="mb-3", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
        dbc.Row(id='constituency-grid', className="g-3 mb-4")
    ])

# Callbacks for dynamic filters
@callback(
    Output('district-filter', 'options'),
    Output('district-filter', 'value'),
    Input('state-filter', 'value'),
    State('lang-store', 'data')
)
def update_district_dropdown(selected_state, lang):
    t = PAGE_TRANSLATIONS.get(lang, PAGE_TRANSLATIONS['en'])
    districts = data_service.get_districts(state=selected_state)
    options = [{'label': t['all_districts'], 'value': 'ALL'}] + [{'label': d, 'value': d} for d in districts]
    return options, 'ALL'

@callback(
    Output('ranking-plot', 'figure'),
    Output('momentum-plot', 'figure'),
    Output('constituency-grid', 'children'),
    Input('state-filter', 'value'),
    Input('district-filter', 'value'),
    Input('risk-filter', 'value'),
    Input('region-type-filter', 'value'),
    Input('search-input', 'value'),
    State('lang-store', 'data')
)
def update_analytics_view(state, district, risk, region_type, search, lang):
    t = PAGE_TRANSLATIONS.get(lang, PAGE_TRANSLATIONS['en'])
    
    filtered_df = data_service.filter_data(
        state=state if state != 'ALL' else None,
        district=district if district != 'ALL' else None,
        risk_level=risk if risk != 'ALL' else None,
        region_type=region_type if region_type != 'ALL' else None,
        search_query=search
    )
    
    # 1. Ranking Chart
    if filtered_df.empty:
        ranking_fig = go.Figure()
        ranking_fig.update_layout(title=t['no_records'])
        momentum_fig = go.Figure()
        momentum_fig.update_layout(title="No data")
        grid_children = [dbc.Col(html.Div(t['no_records'], className="text-muted text-center py-4"), width=12)]
        return ranking_fig, momentum_fig, grid_children
        
    ranking_df = filtered_df.sort_values(by='actual_final_turnout', ascending=False).head(15)
    ranking_fig = go.Figure()
    ranking_fig.add_trace(go.Bar(
        x=ranking_df['constituency'],
        y=ranking_df['actual_final_turnout'],
        name=t['predicted_turnout'],
        marker_color='#2563EB',
        hovertext=ranking_df['district']
    ))
    ranking_fig.add_trace(go.Scatter(
        x=ranking_df['constituency'],
        y=ranking_df['historical_turnout'],
        mode='lines+markers',
        name=t['historical_turnout'],
        line=dict(color='#FACC15', width=2)
    ))
    ranking_fig.update_layout(
        title=dict(text=t['chart_title_perf'], font=dict(color='#F8FAFC', family='Poppins')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        xaxis=dict(gridcolor='#1E293B', tickangle=45),
        yaxis=dict(gridcolor='#1E293B', title="Voter Turnout (%)"),
        margin=dict(l=40, r=20, t=40, b=80),
        legend=dict(font=dict(color='#F8FAFC'))
    )
    
    # 2. Momentum Distribution Chart
    momentum_counts = filtered_df['participation_momentum'].value_counts()
    colors = {
        'Accelerating': '#22C55E',
        'Stable': '#FACC15',
        'Declining': '#EF4444'
    }
    bar_colors = [colors.get(m, '#94A3B8') for m in momentum_counts.index]
    
    # Map index labels to translated momentum strings
    translated_labels = [t.get(m, m) for m in momentum_counts.index]
    
    momentum_fig = go.Figure(data=[go.Bar(
        x=translated_labels,
        y=momentum_counts.values,
        marker_color=bar_colors,
        text=momentum_counts.values,
        textposition='auto'
    )])
    momentum_fig.update_layout(
        title=dict(text=t['chart_title_mom'], font=dict(color='#F8FAFC', family='Poppins')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        xaxis=dict(gridcolor='#1E293B'),
        yaxis=dict(gridcolor='#1E293B', title="No. of Constituencies"),
        margin=dict(l=40, r=20, t=40, b=40)
    )
    
    # 3. Constituency Grid Cards
    grid_children = []
    display_df = filtered_df.head(32)
    for idx, row in display_df.iterrows():
        risk_class = f"risk-{row['risk_level'].lower()}"
        risk_badge_color = 'danger' if row['risk_level'] == 'High' else ('warning' if row['risk_level'] == 'Medium' else 'success')
        momentum_badge_color = 'success' if row['participation_momentum'] == 'Accelerating' else ('warning' if row['participation_momentum'] == 'Stable' else 'danger')
        
        card = dbc.Col([
            dbc.Card([
                html.Div([
                    html.H6(row['constituency'], style={'fontWeight': 'bold', 'margin': 0, 'color': '#F8FAFC'}),
                    html.Span(t.get(row['region_type'], row['region_type']), className="badge bg-secondary ms-2", style={'fontSize': '0.7rem'})
                ], className="d-flex align-items-center justify-content-between mb-2"),
                
                html.Div([
                    html.Span(f"{row['district']}, {row['state']}", style={'fontSize': '0.8rem', 'color': '#94A3B8'})
                ], className="mb-2"),
                
                # Turnout info
                dbc.Row([
                    dbc.Col([
                        html.Div(t['turnout_lbl'], style={'fontSize': '0.7rem', 'color': '#94A3B8'}),
                        html.Div(f"{row['current_turnout']}%", style={'fontWeight': 'bold', 'fontSize': '1.1rem', 'color': '#F8FAFC'})
                    ], xs=6),
                    dbc.Col([
                        html.Div(t['historical_lbl'], style={'fontSize': '0.7rem', 'color': '#94A3B8'}),
                        html.Div(f"{row['historical_turnout']}%", style={'fontWeight': 'bold', 'fontSize': '1.1rem', 'color': '#F8FAFC'})
                    ], xs=6)
                ], className="g-0 mb-3"),
                
                # Badges row
                html.Div([
                    html.Span(f"{t['risk_badge']}: {t.get(row['risk_level'], row['risk_level'])}", className=f"badge bg-{risk_badge_color} me-1", style={'fontSize': '0.7rem'}),
                    html.Span(f"{t['momentum_badge']}: {t.get(row['participation_momentum'], row['participation_momentum'])}", className=f"badge bg-{momentum_badge_color}", style={'fontSize': '0.7rem'}),
                ], className="d-flex")
            ], className=f"stat-card {risk_class}", style={'padding': '1rem'})
        ], xl=3, lg=4, md=6, xs=12)
        grid_children.append(card)
        
    if len(filtered_df) > 32:
        grid_children.append(
            dbc.Col(
                html.Div(t['more_const'].format(count=len(filtered_df) - 32), 
                         className="text-muted text-center py-2", style={'fontSize': '0.85rem'}),
                width=12
            )
        )
        
    return ranking_fig, momentum_fig, grid_children

