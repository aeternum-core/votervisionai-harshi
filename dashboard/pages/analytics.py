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
    
    # State Options
    state_options = [{'label': 'All States', 'value': 'ALL'}] + [{'label': s, 'value': s} for s in states]
    
    # Initial layout
    return html.Div([
        # Header Row
        html.Div([
            html.H3("State & District Drill-Down Analytics", style={'fontFamily': 'Poppins', 'fontWeight': '600', 'color': '#F8FAFC'}),
            html.P("Explore voter engagement, compare region rankings, and view booth level participation alerts.", style={'color': '#94A3B8'})
        ], className="mb-4"),
        
        # Filtering Controls Card
        dbc.Card([
            dbc.Row([
                dbc.Col([
                    html.Label("Filter State", className="form-label-custom"),
                    dcc.Dropdown(
                        id='state-filter',
                        options=state_options,
                        value='ALL',
                        clearable=False,
                        className="bg-dark text-white border-secondary"
                    )
                ], lg=3, md=6, xs=12, className="mb-2"),
                
                dbc.Col([
                    html.Label("Filter District", className="form-label-custom"),
                    dcc.Dropdown(
                        id='district-filter',
                        options=[{'label': 'All Districts', 'value': 'ALL'}],
                        value='ALL',
                        clearable=False,
                        className="bg-dark text-white border-secondary"
                    )
                ], lg=3, md=6, xs=12, className="mb-2"),
                
                dbc.Col([
                    html.Label("Risk Level", className="form-label-custom"),
                    dcc.Dropdown(
                        id='risk-filter',
                        options=[
                            {'label': 'All Risk Levels', 'value': 'ALL'},
                            {'label': '🔴 High Risk', 'value': 'High'},
                            {'label': '🟡 Medium Risk', 'value': 'Medium'},
                            {'label': '🟢 Low Risk', 'value': 'Low'}
                        ],
                        value='ALL',
                        clearable=False,
                        className="bg-dark text-white border-secondary"
                    )
                ], lg=2, md=4, xs=6, className="mb-2"),
                
                dbc.Col([
                    html.Label("Region Type", className="form-label-custom"),
                    dcc.Dropdown(
                        id='region-type-filter',
                        options=[
                            {'label': 'All Types', 'value': 'ALL'},
                            {'label': 'Urban', 'value': 'Urban'},
                            {'label': 'Rural', 'value': 'Rural'}
                        ],
                        value='ALL',
                        clearable=False,
                        className="bg-dark text-white border-secondary"
                    )
                ], lg=2, md=4, xs=6, className="mb-2"),
                
                dbc.Col([
                    html.Label("Search Constituency", className="form-label-custom"),
                    dbc.Input(
                        id='search-input',
                        placeholder="Type to search...",
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
                    dcc.Graph(id='ranking-plot', config={'displayModeBar': False})
                ], className="stat-card mb-4")
            ], xl=8, lg=7, md=12),
            
            dbc.Col([
                html.Div([
                    dcc.Graph(id='momentum-plot', config={'displayModeBar': False})
                ], className="stat-card mb-4")
            ], xl=4, lg=5, md=12)
        ]),
        
        # Grid title and list
        html.H5("Constituency Intelligence Cells", className="mb-3", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
        dbc.Row(id='constituency-grid', className="g-3 mb-4")
    ])

# Callbacks for dynamic filters
@callback(
    Output('district-filter', 'options'),
    Output('district-filter', 'value'),
    Input('state-filter', 'value')
)
def update_district_dropdown(selected_state):
    districts = data_service.get_districts(state=selected_state)
    options = [{'label': 'All Districts', 'value': 'ALL'}] + [{'label': d, 'value': d} for d in districts]
    return options, 'ALL'

@callback(
    Output('ranking-plot', 'figure'),
    Output('momentum-plot', 'figure'),
    Output('constituency-grid', 'children'),
    Input('state-filter', 'value'),
    Input('district-filter', 'value'),
    Input('risk-filter', 'value'),
    Input('region-type-filter', 'value'),
    Input('search-input', 'value')
)
def update_analytics_view(state, district, risk, region_type, search):
    filtered_df = data_service.filter_data(
        state=state if state != 'ALL' else None,
        district=district if district != 'ALL' else None,
        risk_level=risk if risk != 'ALL' else None,
        region_type=region_type if region_type != 'ALL' else None,
        search_query=search
    )
    
    # 1. Ranking Chart (top 15 constituencies by final turnout)
    if filtered_df.empty:
        ranking_fig = go.Figure()
        ranking_fig.update_layout(title="No matching constituencies found")
        momentum_fig = go.Figure()
        momentum_fig.update_layout(title="No data")
        grid_children = [dbc.Col(html.Div("No records found matching current criteria.", className="text-muted text-center py-4"), width=12)]
        return ranking_fig, momentum_fig, grid_children
        
    ranking_df = filtered_df.sort_values(by='actual_final_turnout', ascending=False).head(15)
    ranking_fig = go.Figure()
    ranking_fig.add_trace(go.Bar(
        x=ranking_df['constituency'],
        y=ranking_df['actual_final_turnout'],
        name='Predicted Turnout',
        marker_color='#2563EB',
        hovertext=ranking_df['district']
    ))
    ranking_fig.add_trace(go.Scatter(
        x=ranking_df['constituency'],
        y=ranking_df['historical_turnout'],
        mode='lines+markers',
        name='Historical Turnout',
        line=dict(color='#FACC15', width=2)
    ))
    ranking_fig.update_layout(
        title=dict(text="Top Constituency Performance vs Historical Baseline", font=dict(color='#F8FAFC', family='Poppins')),
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
    
    momentum_fig = go.Figure(data=[go.Bar(
        x=momentum_counts.index,
        y=momentum_counts.values,
        marker_color=bar_colors,
        text=momentum_counts.values,
        textposition='auto'
    )])
    momentum_fig.update_layout(
        title=dict(text="Participation Momentum Distribution", font=dict(color='#F8FAFC', family='Poppins')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94A3B8'),
        xaxis=dict(gridcolor='#1E293B'),
        yaxis=dict(gridcolor='#1E293B', title="No. of Constituencies"),
        margin=dict(l=40, r=20, t=40, b=40)
    )
    
    # 3. Constituency Grid Cards
    grid_children = []
    # limit to max 32 cards for DOM performance, show message if more
    display_df = filtered_df.head(32)
    for idx, row in display_df.iterrows():
        risk_class = f"risk-{row['risk_level'].lower()}"
        risk_badge_color = 'danger' if row['risk_level'] == 'High' else ('warning' if row['risk_level'] == 'Medium' else 'success')
        momentum_badge_color = 'success' if row['participation_momentum'] == 'Accelerating' else ('warning' if row['participation_momentum'] == 'Stable' else 'danger')
        
        card = dbc.Col([
            dbc.Card([
                html.Div([
                    html.H6(row['constituency'], style={'fontWeight': 'bold', 'margin': 0, 'color': '#F8FAFC'}),
                    html.Span(row['region_type'], className="badge bg-secondary ms-2", style={'fontSize': '0.7rem'})
                ], className="d-flex align-items-center justify-content-between mb-2"),
                
                html.Div([
                    html.Span(f"{row['district']}, {row['state']}", style={'fontSize': '0.8rem', 'color': '#94A3B8'})
                ], className="mb-2"),
                
                # Turnout info
                dbc.Row([
                    dbc.Col([
                        html.Div("Turnout", style={'fontSize': '0.7rem', 'color': '#94A3B8'}),
                        html.Div(f"{row['current_turnout']}%", style={'fontWeight': 'bold', 'fontSize': '1.1rem', 'color': '#F8FAFC'})
                    ], xs=6),
                    dbc.Col([
                        html.Div("Historical", style={'fontSize': '0.7rem', 'color': '#94A3B8'}),
                        html.Div(f"{row['historical_turnout']}%", style={'fontWeight': 'bold', 'fontSize': '1.1rem', 'color': '#F8FAFC'})
                    ], xs=6)
                ], className="g-0 mb-3"),
                
                # Badges row
                html.Div([
                    html.Span(f"Risk: {row['risk_level']}", className=f"badge bg-{risk_badge_color} me-1", style={'fontSize': '0.7rem'}),
                    html.Span(f"Momentum: {row['participation_momentum']}", className=f"badge bg-{momentum_badge_color}", style={'fontSize': '0.7rem'}),
                ], className="d-flex")
            ], className=f"stat-card {risk_class}", style={'padding': '1rem'})
        ], xl=3, lg=4, md=6, xs=12)
        grid_children.append(card)
        
    if len(filtered_df) > 32:
        grid_children.append(
            dbc.Col(
                html.Div(f"...and {len(filtered_df) - 32} more constituencies. Refine filters to narrow search.", 
                         className="text-muted text-center py-2", style={'fontSize': '0.85rem'}),
                width=12
            )
        )
        
    return ranking_fig, momentum_fig, grid_children
