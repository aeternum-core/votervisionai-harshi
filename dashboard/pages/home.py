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
        'pulse': 'National Election Pulse™',
        'youth': 'Youth Participation Index™',
        'current': 'Current Turnout',
        'predicted': 'Predicted Turnout',
        'total_const': 'Total Constituencies',
        'voters': 'Registered Voters',
        'health': 'Health Score (EHS)™',
        'alerts': 'Active Alerts',
        'live_feed': 'Live Command Feed',
        'matrix': 'State-Level Participation Matrix',
        'live_progressive': 'Live progressive average',
        'forecast': 'AI Forecast Final',
        'states_lbl': 'Across 15 States',
        'active_lbl': 'Active registrations',
        'health_lbl': 'National Avg Health',
        'alert_lbl': 'Risky constituencies',
        'chart_progression': 'Hourly Voter Turnout Progression Trend',
        'chart_risk': 'Voter Turnout Risk Proportions',
        'tbl_state': 'State',
        'tbl_registered': 'Registered Voters',
        'tbl_current': 'Current Turnout',
        'tbl_historical': 'Historical Avg',
        'tbl_health': 'Health Score',
        'tbl_status': 'Status',
        'tbl_zones': 'High Risk Zones',
        'no_data': 'No data available. Please generate synthetic data in Admin panel.'
    },
    'hi': {
        'pulse': 'राष्ट्रीय चुनाव पल्स™',
        'youth': 'युवा भागीदारी सूचकांक™',
        'current': 'वर्तमान मतदान',
        'predicted': 'पूर्वानुमानित मतदान',
        'total_const': 'कुल निर्वाचन क्षेत्र',
        'voters': 'पंजीकृत मतदाता',
        'health': 'स्वास्थ्य स्कोर (EHS)™',
        'alerts': 'सक्रिय अलर्ट',
        'live_feed': 'लाइव कमांड फीड',
        'matrix': 'राज्य-स्तरीय भागीदारी मैट्रिक्स',
        'live_progressive': 'लाइव प्रगतिशील औसत',
        'forecast': 'एआई अंतिम पूर्वानुमान',
        'states_lbl': '15 राज्यों में',
        'active_lbl': 'सक्रिय पंजीकरण',
        'health_lbl': 'राष्ट्रीय औसत स्वास्थ्य',
        'alert_lbl': 'जोखिम वाले निर्वाचन क्षेत्र',
        'chart_progression': 'प्रति घंटा मतदान प्रगति की प्रवृत्ति',
        'chart_risk': 'मतदान जोखिम अनुपात',
        'tbl_state': 'राज्य',
        'tbl_registered': 'पंजीकृत मतदाता',
        'tbl_current': 'वर्तमान मतदान',
        'tbl_historical': 'ऐतिहासिक औसत',
        'tbl_health': 'स्वास्थ्य स्कोर',
        'tbl_status': 'स्थिति',
        'tbl_zones': 'उच्च जोखिम क्षेत्र',
        'no_data': 'कोई डेटा उपलब्ध नहीं है। कृपया एडमिन पैनल में डेटा उत्पन्न करें।'
    },
    'kn': {
        'pulse': 'ರಾಷ್ಟ್ರೀಯ ಚುನಾವಣಾ ಪಲ್ಸ್™',
        'youth': 'ಯುವ ಭಾಗವಹಿಸುವಿಕೆ ಸೂಚ್ಯಂಕ™',
        'current': 'ಪ್ರಸ್ತುತ ಮತದಾನ',
        'predicted': 'ಮುನ್ಸೂಚಿತ ಮತದಾನ',
        'total_const': 'ಒಟ್ಟು ಮತಕ್ಷೇತ್ರಗಳು',
        'voters': 'ನೊಂದಾಯಿತ ಮತದಾರರು',
        'health': 'ಆರೋಗ್ಯ ಸ್ಕೋರ್ (EHS)™',
        'alerts': 'ಸಕ್ರಿಯ ಎಚ್ಚರಿಕೆಗಳು',
        'live_feed': 'ಲೈವ್ ಕಮಾಂಡ್ ಫೀಡ್',
        'matrix': 'ರಾಜ್ಯ ಮಟ್ಟದ ಭಾಗವಹಿಸುವಿಕೆ ಮ್ಯಾಟ್ರಿಕ್ಸ್',
        'live_progressive': 'ಲೈವ್ ಪ್ರಗತಿಶೀಲ ಸರಾಸರಿ',
        'forecast': 'ಎಐ ಅಂತಿಮ ಮುನ್ಸೂಚನೆ',
        'states_lbl': '15 ರಾಜ್ಯಗಳಲ್ಲಿ',
        'active_lbl': 'ಸಕ್ರಿಯ ನೊಂದಣಿಗಳು',
        'health_lbl': 'ರಾಷ್ಟ್ರೀಯ ಸರಾಸರಿ ಆರೋಗ್ಯ',
        'alert_lbl': 'ಅಪಾಯದ ಮತಕ್ಷೇತ್ರಗಳು',
        'chart_progression': 'ಗಂಟೆಯ ಮತದಾರರ ಭಾಗವಹಿಸುವಿಕೆಯ ವೇಗ',
        'chart_risk': 'ಮತದಾರರ ಅಪಾಯದ ಅನುಪಾತಗಳು',
        'tbl_state': 'ರಾಜ್ಯ',
        'tbl_registered': 'ನೊಂದಾಯಿತ ಮತದಾರರು',
        'tbl_current': 'ಪ್ರಸ್ತುತ ಮತದಾನ',
        'tbl_historical': 'ಐತಿಹಾಸಿಕ ಸರಾಸರಿ',
        'tbl_health': 'ಆರೋಗ್ಯ ಸ್ಕೋರ್',
        'tbl_status': 'ಸ್ಥಿತಿ',
        'tbl_zones': 'ಹೆಚ್ಚಿನ ಅಪಾಯದ ವಲಯಗಳು',
        'no_data': 'ಯಾವುದೇ ಡೇಟಾ ಲಭ್ಯವಿಲ್ಲ. ದಯವಿಟ್ಟು ಡೇಟಾವನ್ನು ನಿರ್ವಹಣಾ ಫಲಕದಲ್ಲಿ ರಚಿಸಿ.'
    }
}

def get_layout(lang='en'):
    # Load translation labels
    texts = config.LANGUAGES.get(lang, config.LANGUAGES['en'])
    t = PAGE_TRANSLATIONS.get(lang, PAGE_TRANSLATIONS['en'])
    stats = data_service.get_national_stats()
    
    if not stats:
        return html.Div(t['no_data'], style={'color': 'white', 'padding': '2rem'})
    
    # Live feed events
    feed_items = data_service.get_live_feed()
    feed_components = []
    for item in feed_items:
        badge_class = f"badge-{item['type']}"
        feed_components.append(
            html.Div([
                html.Span(item['time'], className="badge bg-secondary me-2"),
                html.Span(item['message'], style={'color': '#F8FAFC'}),
                html.Span(item['type'].upper(), className=f"badge {badge_class} ms-auto", style={'fontSize': '0.7rem'})
            ], className="ticker-item d-flex align-items-center")
        )

    # 1. Grid of KPI cards (2 rows of 4 cards)
    kpi_cards = html.Div([
        dbc.Row([
            dbc.Col(dbc.Card([
                html.Div(t['pulse'], className="card-title-custom", style={'color': '#60A5FA'}),
                html.Div(f"{stats['pulse_score']}/100", className="card-value-custom", style={'color': '#60A5FA'}),
                html.Div(stats['pulse_status'], style={'fontSize': '0.75rem', 'fontWeight': 'bold', 'color': '#22C55E' if stats['pulse_score'] >= 80 else '#FACC15'})
            ], className="stat-card h-100")),
            dbc.Col(dbc.Card([
                html.Div(t['youth'], className="card-title-custom", style={'color': '#FACC15'}),
                html.Div(f"{stats['ypi_score']}/100", className="card-value-custom", style={'color': '#FACC15'}),
                html.Div(stats['ypi_status'], style={'fontSize': '0.75rem', 'fontWeight': 'bold', 'color': '#22C55E' if stats['ypi_score'] >= 75 else '#FACC15'})
            ], className="stat-card h-100")),
            dbc.Col(dbc.Card([
                html.Div(t['current'], className="card-title-custom"),
                html.Div(f"{stats['current_turnout']}%", className="card-value-custom"),
                html.Div(t['live_progressive'], className="text-muted", style={'fontSize': '0.75rem'})
            ], className="stat-card h-100")),
            dbc.Col(dbc.Card([
                html.Div(t['predicted'], className="card-title-custom"),
                html.Div(f"{stats['predicted_turnout']}%", className="card-value-custom", style={'color': '#3B82F6'}),
                html.Div(t['forecast'], className="text-muted", style={'fontSize': '0.75rem'})
            ], className="stat-card h-100")),
        ], className="mb-3 g-3"),
        dbc.Row([
            dbc.Col(dbc.Card([
                html.Div(t['total_const'], className="card-title-custom"),
                html.Div(f"{stats['total_regions']}", className="card-value-custom"),
                html.Div(t['states_lbl'], className="text-muted", style={'fontSize': '0.75rem'})
            ], className="stat-card h-100")),
            dbc.Col(dbc.Card([
                html.Div(t['voters'], className="card-title-custom"),
                html.Div(f"{stats['registered_voters']:,}", className="card-value-custom", style={'fontSize': '1.5rem'}),
                html.Div(t['active_lbl'], className="text-muted", style={'fontSize': '0.75rem'})
            ], className="stat-card h-100")),
            dbc.Col(dbc.Card([
                html.Div(t['health'], className="card-title-custom"),
                html.Div(f"{stats['health_score']}/100", className="card-value-custom", style={'color': '#22C55E' if stats['health_score'] >= 75 else '#FACC15'}),
                html.Div(t['health_lbl'], className="text-muted", style={'fontSize': '0.75rem'})
            ], className="stat-card h-100")),
            dbc.Col(dbc.Card([
                html.Div(t['alerts'], className="card-title-custom"),
                html.Div(f"{stats['active_alerts']}", className="card-value-custom", style={'color': '#EF4444' if stats['active_alerts'] > 5 else '#FACC15'}),
                html.Div(t['alert_lbl'], className="text-muted", style={'fontSize': '0.75rem'})
            ], className="stat-card h-100")),
        ], className="mb-4 g-3")
    ])

    # Load plots
    df = data_service.df
    
    # 2. Plot 1: Turnout progression hourly comparison
    progression_fig = go.Figure()
    hours = ['9 AM', '11 AM', '1 PM', '3 PM', '5 PM']
    
    # Calculate hourly averages
    avg_9am = df['turnout_9am'].mean()
    avg_11am = df['turnout_11am'].mean()
    avg_1pm = df['turnout_1pm'].mean()
    avg_3pm = df['turnout_3pm'].mean()
    avg_5pm = df['turnout_5pm'].mean()
    
    # Add actual/historical benchmarks
    hist_avg = df['historical_turnout'].mean()
    # Historical curve estimate
    hist_curve = [hist_avg * p for p in [0.21, 0.43, 0.61, 0.78, 0.93]]
    
    progression_fig.add_trace(go.Scatter(
        x=hours, y=[avg_9am, avg_11am, avg_1pm, avg_3pm, avg_5pm],
        mode='lines+markers', name='Current Live Turnout',
        line=dict(color='#2563EB', width=3),
        marker=dict(size=8, color='#60A5FA')
    ))
    progression_fig.add_trace(go.Scatter(
        x=hours, y=hist_curve,
        mode='lines+markers', name='Historical Benchmark',
        line=dict(color='#94A3B8', width=2, dash='dash')
    ))
    
    progression_fig.update_layout(
        title=dict(text=t['chart_progression'], font=dict(color='#F8FAFC', family='Poppins')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        xaxis=dict(gridcolor='#1E293B'),
        yaxis=dict(gridcolor='#1E293B', title="Turnout Percentage (%)"),
        legend=dict(font=dict(color='#F8FAFC')),
        margin=dict(l=40, r=20, t=40, b=30)
    )

    # 3. Plot 2: Risk distribution donut chart
    risk_counts = df['risk_level'].value_counts()
    risk_fig = go.Figure(data=[go.Pie(
        labels=risk_counts.index,
        values=risk_counts.values,
        hole=.4,
        marker=dict(colors=['#22C55E', '#FACC15', '#EF4444']),
        textinfo='percent+label',
        textfont=dict(color='#0B1220')
    )])
    risk_fig.update_layout(
        title=dict(text=t['chart_risk'], font=dict(color='#F8FAFC', family='Poppins')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        legend=dict(font=dict(color='#F8FAFC')),
        margin=dict(l=20, r=20, t=40, b=30)
    )

    # 4. State Summary Table
    state_groups = df.groupby('state').agg({
        'registered_voters': 'sum',
        'current_turnout': 'mean',
        'actual_final_turnout': 'mean',
        'election_health_score': 'mean',
        'risk_level': lambda x: (x == 'High').sum()
    }).reset_index()
    
    table_rows = []
    for idx, row in state_groups.iterrows():
        health = round(row['election_health_score'], 1)
        health_color = '#22C55E' if health >= 75 else '#FACC15'
        risk_badge = html.Span(f"{row['risk_level']} {t['tbl_zones']}", 
                               className="badge bg-danger" if row['risk_level'] > 0 else "badge bg-success")
        
        table_rows.append(html.Tr([
            html.Td(row['state'], style={'fontWeight': '600'}),
            html.Td(f"{int(row['registered_voters']):,}"),
            html.Td(f"{round(row['current_turnout'], 1)}%"),
            html.Td(f"{round(row['actual_final_turnout'], 1)}%"),
            html.Td(f"{health}/100", style={'color': health_color, 'fontWeight': 'bold'}),
            html.Td(risk_badge)
        ]))

    state_table = dbc.Table([
        html.Thead(html.Tr([
            html.Th(t['tbl_state']), html.Th(t['tbl_registered']), html.Th(t['tbl_current']), 
            html.Th(t['tbl_historical']), html.Th(t['tbl_health']), html.Th(t['tbl_status'])
        ]))] + [html.Tbody(table_rows)],
        className="table-custom",
        bordered=False,
        hover=True,
        responsive=True
    )

    layout = html.Div([
        # Hero Section
        html.Div([
            html.H2(texts['title'], className="sidebar-title", style={'fontSize': '2rem'}),
            html.P(texts['tagline'], style={'color': '#94A3B8', 'fontSize': '1rem', 'marginBottom': '1.5rem'}),
        ], className="mb-4"),
        
        # KPI Grid
        kpi_cards,
        
        # Graphs and Live Feed
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(figure=progression_fig, config={'displayModeBar': False, 'responsive': True})
                ], className="stat-card mb-4")
            ], xl=8, lg=7, md=12),
            
            dbc.Col([
                html.Div([
                    html.H5(t['live_feed'], className="mb-3", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
                    html.Div(feed_components, className="ticker-container")
                ], className="stat-card mb-4", style={'height': 'calc(100% - 1.5rem)'})
            ], xl=4, lg=5, md=12)
        ]),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(figure=risk_fig, config={'displayModeBar': False, 'responsive': True})
                ], className="stat-card mb-4")
            ], xl=4, lg=5, md=12),
            
            dbc.Col([
                html.Div([
                    html.H5(t['matrix'], className="mb-3", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
                    state_table
                ], className="stat-card mb-4", style={'height': 'calc(100% - 1.5rem)'})
            ], xl=8, lg=7, md=12)
        ])
    ])
    
    return layout
