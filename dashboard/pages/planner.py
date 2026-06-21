from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
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
    
    # Static summary card on intervention methodology
    methods_card = dbc.Card([
        html.H5("Election Strategy Advisor™ Prescriptions", className="mb-3", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
        html.P("Our AI evaluates live socio-economic deficits and polling progression to recommend targeted voter turnout recovery plans:", style={'fontSize': '0.85rem', 'color': '#94A3B8'}),
        html.Ul([
            html.Li("If accessibility scores are low -> deploy polling station transport shuttles.", style={'fontSize': '0.8rem', 'marginBottom': '0.3rem'}),
            html.Li("If youth demographics are high but turnout is low -> launch targeted social media micro-campaigns.", style={'fontSize': '0.8rem', 'marginBottom': '0.3rem'}),
            html.Li("If weather scores are under 50 -> set up heat/rain queue canopies and water kiosks.", style={'fontSize': '0.8rem', 'marginBottom': '0.3rem'}),
            html.Li("If overall awareness is low -> deploy door-to-door volunteers and local language audio boards.", style={'fontSize': '0.8rem'})
        ], className="ps-3 mb-0")
    ], className="stat-card p-4 h-100")

    return html.Div([
        # Header
        html.Div([
            html.H3("Election Strategy Advisor™", style={'fontFamily': 'Poppins', 'fontWeight': '600', 'color': '#F8FAFC'}),
            html.P("Access prescriptive strategy actions mapped to specific regional voter participation barriers to systematically boost democracy.", style={'color': '#94A3B8'})
        ], className="mb-4"),
        
        # Row 1: Filters & Explanation
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.Label("Select Target State", className="form-label-custom"),
                    dcc.Dropdown(
                        id='plan-state-filter',
                        options=state_options,
                        value='ALL',
                        clearable=False,
                        className="bg-dark text-white border-secondary mb-4"
                    ),
                    html.Label("Intervention Priority Threshold", className="form-label-custom"),
                    dcc.Dropdown(
                        id='plan-priority-filter',
                        options=[
                            {'label': 'High Priority (Priority Index > 15)', 'value': 'high'},
                            {'label': 'Show All Needs', 'value': 'all'}
                        ],
                        value='all',
                        clearable=False,
                        className="bg-dark text-white border-secondary"
                    )
                ], className="stat-card p-4 h-100 overflow-visible")
            ], lg=4, md=12, className="mb-4"),
            
            dbc.Col(methods_card, lg=8, md=12, className="mb-4")
        ]),
        
        # Priority Queue header
        html.Div([
            html.H5("Ranked Strategic Interventions Queue", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
            dbc.Button("Export Strategy Report (CSV)", id='plan-export-btn', color="primary", size="sm", className="ms-auto", style={'fontWeight': '500'})
        ], className="d-flex align-items-center justify-content-between mb-3"),
        
        # List Container
        html.Div(id='plan-queue-container')
    ])

@callback(
    Output('plan-queue-container', 'children'),
    Input('plan-state-filter', 'value'),
    Input('plan-priority-filter', 'value')
)
def update_planner_queue(selected_state, priority_threshold):
    recommendations = data_service.get_interventions(
        state=selected_state if selected_state != 'ALL' else None,
        limit=25
    )
    
    if not recommendations:
        return html.Div("No areas require urgent intervention.", className="text-muted text-center py-4")
        
    # Apply threshold if requested
    if priority_threshold == 'high':
        recommendations = [r for r in recommendations if r['priority_score'] > 15]
        
    if not recommendations:
        return html.Div("No active areas match high priority criteria (Priority Index > 15).", className="text-muted text-center py-4")
        
    cards = []
    for idx, r in enumerate(recommendations):
        rank = idx + 1
        risk_color = 'danger' if r['risk_level'] == 'High' else ('warning' if r['risk_level'] == 'Medium' else 'success')
        
        action_boxes = []
        for action in r['actions']:
            action_boxes.append(
                dbc.Col([
                    html.Div([
                        html.Div(action['action'], style={'fontWeight': '600', 'color': '#F8FAFC', 'fontSize': '0.9rem'}),
                        html.Div(action['reason'], style={'fontSize': '0.75rem', 'color': '#94A3B8', 'marginTop': '0.2rem'}),
                        html.Div([
                            html.Span(f"Expected Gain: {action['impact']}", className="badge bg-success text-white me-2", style={'fontSize': '0.7rem', 'backgroundColor': 'rgba(34, 197, 94, 0.15) !important'}),
                            html.Span(f"Difficulty: {action['difficulty']}", className="badge bg-secondary", style={'fontSize': '0.7rem'})
                        ], className="d-flex mt-2")
                    ], className="border border-secondary rounded p-3 mb-2 h-100", style={'backgroundColor': '#0F1626'})
                ], md=6, xs=12)
            )
            
        card = dbc.Card([
            dbc.Row([
                # Left Rank and Meta Col
                dbc.Col([
                    html.Div([
                        html.Div(f"#{rank}", style={'fontSize': '1.8rem', 'fontWeight': 'bold', 'color': '#60A5FA', 'fontFamily': 'Poppins'}),
                        html.Div("STRATEGIC RANK", style={'fontSize': '0.65rem', 'color': '#94A3B8'})
                    ], className="text-center mb-2"),
                    
                    html.Div([
                        html.Span(f"Priority Index: {r['priority_score']:.1f}", className="badge bg-dark border border-secondary text-light", style={'fontSize': '0.75rem'})
                    ], className="text-center")
                ], xl=2, lg=2, md=3, xs=4, className="d-flex flex-column justify-content-center border-end border-secondary py-2"),
                
                # Middle Info Col
                dbc.Col([
                    html.H5(r['constituency'], style={'fontWeight': 'bold', 'color': '#F8FAFC', 'margin': 0}),
                    html.P(f"{r['district']} district, {r['state']}", style={'color': '#94A3B8', 'fontSize': '0.8rem', 'marginBottom': '0.8rem'}),
                    
                    dbc.Row([
                        dbc.Col([
                            html.Div("Early Turnout", style={'fontSize': '0.7rem', 'color': '#94A3B8'}),
                            html.Div(f"{r['current_turnout']}%", style={'fontWeight': 'bold', 'fontSize': '1.0rem', 'color': '#F8FAFC'})
                        ], xs=4),
                        dbc.Col([
                            html.Div("Historical Target", style={'fontSize': '0.7rem', 'color': '#94A3B8'}),
                            html.Div(f"{r['historical_turnout']}%", style={'fontWeight': 'bold', 'fontSize': '1.0rem', 'color': '#F8FAFC'})
                        ], xs=4),
                        dbc.Col([
                            html.Div("Risk Rating", style={'fontSize': '0.7rem', 'color': '#94A3B8'}),
                            html.Span(r['risk_level'], className=f"badge bg-{risk_color} mt-1", style={'fontSize': '0.75rem'})
                        ], xs=4)
                    ], className="g-0 mb-2"),
                    
                    # Diagnosed Issue line
                    html.Div([
                        html.Span("Diagnosed Barrier: ", style={'fontSize': '0.75rem', 'color': '#94A3B8'}),
                        html.Span(r['primary_issue'], style={'fontSize': '0.8rem', 'color': '#FACC15', 'fontWeight': '600'})
                    ], className="border-top border-secondary pt-2", style={'borderColor': 'rgba(30, 41, 59, 0.4)'})
                ], xl=4, lg=4, md=5, xs=8, className="ps-3 py-2"),
                
                # Right Actions Col
                dbc.Col([
                    html.Div("PRESCRIPTIVE ACTION RECIPES", className="card-title-custom mb-2", style={'fontSize': '0.75rem'}),
                    dbc.Row(action_boxes, className="g-2")
                ], xl=6, lg=6, md=12, xs=12, className="py-2")
            ], className="g-0 align-items-center")
        ], className="stat-card mb-3", style={'padding': '1rem 1.5rem'})
        
        cards.append(card)
        
    return html.Div(cards)
