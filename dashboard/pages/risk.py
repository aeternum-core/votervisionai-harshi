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
    state_options = [{'label': 'All States', 'value': 'ALL'}] + [{'label': s, 'value': s} for s in states]
    
    # Grid Layout
    return html.Div([
        # Header Row
        html.Div([
            html.H3("AI Risk Intelligence Center", style={'fontFamily': 'Poppins', 'fontWeight': '600', 'color': '#F8FAFC'}),
            html.P("Monitor real-time participation risk indices, investigate underperforming voting corridors, and prioritize awareness efforts.", style={'color': '#94A3B8'})
        ], className="mb-4"),
        
        # Risk Filters
        dbc.Card([
            dbc.Row([
                dbc.Col([
                    html.Label("Inspect State", className="form-label-custom"),
                    dcc.Dropdown(
                        id='risk-state-filter',
                        options=state_options,
                        value='ALL',
                        clearable=False,
                        className="bg-dark text-white border-secondary"
                    )
                ], md=4, xs=12),
                
                dbc.Col([
                    html.Label("Priority Category", className="form-label-custom"),
                    dcc.Dropdown(
                        id='risk-category-filter',
                        options=[
                            {'label': 'All Risk Categories', 'value': 'ALL'},
                            {'label': 'Turnout Slowdown (Deficit > 3%)', 'value': 'slowdown'},
                            {'label': 'Awareness Deficit (Awareness < 60)', 'value': 'awareness'},
                            {'label': 'Infrastructure / Access Gaps', 'value': 'infrastructure'},
                            {'label': 'Severe Weather Gaps', 'value': 'weather'}
                        ],
                        value='ALL',
                        clearable=False,
                        className="bg-dark text-white border-secondary"
                    )
                ], md=4, xs=12),
                
                dbc.Col([
                    html.Label("Search Risk Zones", className="form-label-custom"),
                    dbc.Input(
                        id='risk-search-input',
                        placeholder="Type constituency name...",
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
                    html.H5("Active Risk Summary", className="mb-4", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
                    html.Div(id='risk-metrics-panel')
                ], className="stat-card mb-4", style={'height': 'calc(100% - 1.5rem)'})
            ], xl=4, lg=5, md=12)
        ]),
        
        # Risk Table Grid
        html.H5("Critical Risk Operations Log", className="mb-3", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
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
    Input('risk-search-input', 'value')
)
def update_risk_dashboard(selected_state, selected_category, search_query):
    # Filter dataset
    df = data_service.df
    if df.empty:
        return go.Figure(), html.Div("No data"), html.Div("No data")
        
    filtered = df.copy()
    if selected_state and selected_state != 'ALL':
        filtered = filtered[filtered['state'] == selected_state]
        
    # Apply category logic
    if selected_category == 'slowdown':
        # deficit = historical - current
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
                html.Div("HIGH RISK ZONES", style={'fontSize': '0.75rem', 'color': '#94A3B8'}),
                html.Div(f"{total_high}", style={'fontSize': '1.8rem', 'fontWeight': 'bold', 'color': '#EF4444'})
            ], xs=6),
            dbc.Col([
                html.Div("MEDIUM RISK ZONES", style={'fontSize': '0.75rem', 'color': '#94A3B8'}),
                html.Div(f"{total_med}", style={'fontSize': '1.8rem', 'fontWeight': 'bold', 'color': '#FACC15'})
            ], xs=6)
        ], className="g-0 mb-4"),
        
        html.Div([
            html.Div("AVERAGE PARTICIPATION DEFICIT", style={'fontSize': '0.75rem', 'color': '#94A3B8'}),
            html.Div(f"{avg_deficit:.2f}% below baseline", style={'fontSize': '1.2rem', 'fontWeight': '600', 'color': '#F8FAFC'}),
            html.Div("Compared to historical averages", style={'fontSize': '0.7rem', 'color': '#94A3B8'})
        ], className="mb-4"),
        
        html.Div([
            html.Div("PRIMARY TRIGGER CORRELATION", style={'fontSize': '0.75rem', 'color': '#94A3B8'}),
            # Simple rule-based trigger analysis for selected subset
            html.Ul([
                html.Li(f"Weather impact present in {int((filtered['weather_score'] < 50).sum())} areas.", style={'fontSize': '0.8rem', 'color': '#F8FAFC', 'marginBottom': '0.3rem'}),
                html.Li(f"Awareness deficits found in {int((filtered['awareness_score'] < 60).sum())} areas.", style={'fontSize': '0.8rem', 'color': '#F8FAFC', 'marginBottom': '0.3rem'}),
                html.Li(f"Accessibility barriers found in {int((filtered['transport_accessibility'] < 60).sum())} areas.", style={'fontSize': '0.8rem', 'color': '#F8FAFC'})
            ], className="ps-3 mt-1")
        ])
    ])
    
    # 2. Risk Zones Chart (Top 12 underperforming zones)
    chart_df = filtered.head(12)
    chart_fig = go.Figure()
    
    if chart_df.empty:
        chart_fig.update_layout(title="No at-risk zones match current filters")
    else:
        chart_fig.add_trace(go.Bar(
            x=chart_df['constituency'],
            y=chart_df['turnout_deficit'],
            marker_color='#EF4444',
            name='Turnout Deficit (%)'
        ))
        chart_fig.update_layout(
            title=dict(text="Top Turnout Deficits (Baseline vs Live)", font=dict(color='#F8FAFC', family='Poppins')),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94A3B8'),
            xaxis=dict(gridcolor='#1E293B', tickangle=45),
            yaxis=dict(gridcolor='#1E293B', title="Deficit Percentage (Lower is Better)"),
            margin=dict(l=40, r=20, t=40, b=80)
        )
        
    # 3. Log Table
    table_rows = []
    if filtered.empty:
        table_rows.append(html.Tr([html.Td("No active risk zones identified for current criteria.", colSpan=7, className="text-center text-muted")]))
    else:
        # Display top 15 risk rows in table
        for idx, row in filtered.head(15).iterrows():
            deficit_val = row['turnout_deficit']
            deficit_color = '#EF4444' if deficit_val > 3.0 else '#FACC15'
            
            risk_badge = html.Span(row['risk_level'], className=f"badge bg-{'danger' if row['risk_level'] == 'High' else 'warning'}")
            
            # Diagnose primary trigger
            triggers = []
            if row['weather_score'] < 50:
                triggers.append("Weather")
            if row['awareness_score'] < 60:
                triggers.append("Awareness Gaps")
            if row['transport_accessibility'] < 60:
                triggers.append("Transport Gaps")
            if not triggers:
                triggers.append("Apathy")
                
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
            html.Th("Constituency"), html.Th("District"), html.Th("State"), 
            html.Th("Current Turnout"), html.Th("Historical Turnout"), html.Th("Turnout Deviation"),
            html.Th("Risk Classification"), html.Th("Primary Triggers")
        ]))] + [html.Tbody(table_rows)],
        className="table-custom",
        bordered=False,
        hover=True,
        responsive=True
    )
    
    return chart_fig, metrics_layout, log_table
