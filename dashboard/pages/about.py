from dash import html
import dash_bootstrap_components as dbc
import sys
import os

# Ensure parent directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import config

def get_layout(lang='en'):
    # Comparative Matrix rows
    matrix_rows = [
        html.Tr([html.Td("Turnout Analytics", style={'fontWeight': 'bold'}), html.Td("Descriptive: Reports past turnout percentages only."), html.Td("Predictive & Prescriptive: Forecasts live progressive outcomes and recommends turnout recovery plans.", style={'color': '#60A5FA', 'fontWeight': '600'})]),
        html.Tr([html.Td("Decision Support", style={'fontWeight': 'bold'}), html.Td("None: Static dashboard reports metrics."), html.Td("Prescriptive: Mapped administrative strategies based on socio-economic barriers.", style={'color': '#60A5FA', 'fontWeight': '600'})]),
        html.Tr([html.Td("Operational Simulator", style={'fontWeight': 'bold'}), html.Td("None: No scenario evaluation possible."), html.Td("Simulation: Live What-If Sandbox to test effects of campaigns, transport shuttles, and weather adjustments.", style={'color': '#60A5FA', 'fontWeight': '600'})]),
        html.Tr([html.Td("Risk Detection", style={'fontWeight': 'bold'}), html.Td("Manual: Analysts must visually isolate drops."), html.Td("AI Risk Detector: Automatic anomaly alert indexing for early warnings.", style={'color': '#60A5FA', 'fontWeight': '600'})]),
        html.Tr([html.Td("India Specific Relevance", style={'fontWeight': 'bold'}), html.Td("Generic: Overall global demographic views."), html.Td("Targeted: State/District drilldown, multilingual presets, and Youth Participation Index™.", style={'color': '#60A5FA', 'fontWeight': '600'})])
    ]
    
    comparative_table = dbc.Table([
        html.Thead(html.Tr([
            html.Th("Feature Audit", style={'width': '20%'}),
            html.Th("Existing Election Systems", style={'width': '40%'}),
            html.Th("VoteVision AI (Proposed)", style={'width': '40%'})
        ]))] + [html.Tbody(matrix_rows)],
        className="table-custom mt-3",
        bordered=False,
        hover=True,
        responsive=True
    )

    return html.Div([
        # Header
        html.Div([
            html.H3("Methodology & Innovation Blueprint", style={'fontFamily': 'Poppins', 'fontWeight': '600', 'color': '#F8FAFC'}),
            html.P("Project objectives, comparison matrix, algorithm audits, and official disclosure notices for VoteVision AI.", style={'color': '#94A3B8'})
        ], className="mb-4"),
        
        # Innovation Highlights Card
        dbc.Card([
            html.H5("Innovation Statement", className="mb-3", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
            html.P([
                "Traditional dashboards mainly focus on ", html.Strong("Descriptive Analytics", style={'color': '#94A3B8'}), 
                " (displaying historic and early turnout figures after they occur). ",
                html.Span("VoteVision AI", style={'fontWeight': '700', 'color': '#2563EB'}), 
                " transforms election analytics into ", html.Strong("Predictive Intelligence", style={'color': '#60A5FA'}), " (forecasting final turnout using Machine Learning) and ", 
                html.Strong("Prescriptive Intelligence", style={'color': '#22C55E'}), " (diagnosing regional barriers and recommending action recipes to administrative officers)."
            ], style={'fontSize': '0.9rem', 'lineHeight': '1.5', 'color': '#E2E8F0', 'margin': 0})
        ], className="stat-card p-4 mb-4"),
        
        # Creator Profile & Core Features Card
        dbc.Card([
            dbc.Row([
                dbc.Col([
                    html.H5("Developer Profile", className="mb-3", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
                    html.Div([
                        html.Div([
                            html.Div("Harshitha C", style={'fontSize': '1.3rem', 'fontWeight': 'bold', 'color': '#60A5FA', 'fontFamily': 'Poppins'}),
                            html.Div("Lead Architect & Developer", style={'fontSize': '0.85rem', 'color': '#94A3B8', 'fontWeight': '500', 'textTransform': 'uppercase', 'letterSpacing': '0.05em'})
                        ], className="mb-3"),
                        html.P("Harshitha C designed and developed the VoteVision AI platform to modernize election analytics. By blending machine learning models, descriptive data services, and explainable AI insights, the platform offers election organizers tools for predicting turnout anomalies and optimizing civic engagement strategies.", 
                               style={'fontSize': '0.85rem', 'lineHeight': '1.5', 'color': '#E2E8F0'}),
                        html.Div([
                            html.Span("Python / Dash", className="badge bg-secondary me-2", style={'fontSize': '0.75rem'}),
                            html.Span("Scikit-Learn ML", className="badge bg-secondary me-2", style={'fontSize': '0.75rem'}),
                            html.Span("Data Visualization", className="badge bg-secondary", style={'fontSize': '0.75rem'})
                        ], className="mt-3")
                    ])
                ], lg=5, md=12, className="border-end border-secondary pe-lg-4 mb-4 mb-lg-0"),
                
                dbc.Col([
                    html.H5("Core Platform Features", className="mb-3", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
                    dbc.Row([
                        dbc.Col([
                            html.Ul([
                                html.Li([html.Strong("National Election Pulse™: "), "A live aggregate turnout health indicator (Pulse Score out of 100) combining forecasted risk scores and averages."], style={'fontSize': '0.8rem', 'color': '#E2E8F0', 'marginBottom': '0.5rem'}),
                                html.Li([html.Strong("AI Turnout Forecasts: "), "Uses Random Forest Regressors to forecast final turnout and interactive Plotly speedometers to show prediction confidence."], style={'fontSize': '0.8rem', 'color': '#E2E8F0', 'marginBottom': '0.5rem'}),
                                html.Li([html.Strong("Explainable AI (XAI) Panel: "), "Calculates local feature contribution drivers (transport accessibility, campaign boosts, holidays, weather) for trust validation."], style={'fontSize': '0.8rem', 'color': '#E2E8F0'})
                            ], className="ps-3 mb-3 mb-md-0")
                        ], md=6),
                        dbc.Col([
                            html.Ul([
                                html.Li([html.Strong("What-If Simulator Sandbox: "), "Test adjustments to campaign intensity, transport, or weather comfort, with quick-apply presets (Torrential Rain, Holiday Drag)."], style={'fontSize': '0.8rem', 'color': '#E2E8F0', 'marginBottom': '0.5rem'}),
                                html.Li([html.Strong("Election Strategy Advisor™: "), "Diagnoses local civic barriers and ranks constituencies in a prioritized strategy recommendation log."], style={'fontSize': '0.8rem', 'color': '#E2E8F0', 'marginBottom': '0.5rem'}),
                                html.Li([html.Strong("AI Risk Intelligence: "), "Flags underperforming zones based on historical baseline deviations and registers them in a central operations log."], style={'fontSize': '0.8rem', 'color': '#E2E8F0'})
                            ], className="ps-3")
                        ], md=6)
                    ])
                ], lg=7, md=12, className="ps-lg-4")
            ])
        ], className="stat-card p-4 mb-4"),
        
        dbc.Row([
            # Left: Stack & Formulas
            dbc.Col([
                dbc.Card([
                    html.H5("System Formula Audits", className="mb-4", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
                    
                    html.Div([
                        html.H6("1. National Election Pulse™", style={'fontWeight': '600', 'color': '#60A5FA'}),
                        html.P("Overall participation velocity indicator based on turnout, EHS index, and risk values:", style={'fontSize': '0.8rem', 'color': '#94A3B8'}),
                        html.Code(
                            "Pulse = 0.6*Turnout_Forecast + 0.3*EHS_Avg + 0.1*(1 - High_Risk_Ratio)*100",
                            style={'backgroundColor': '#0F1626', 'padding': '0.5rem 1rem', 'borderRadius': '4px', 'display': 'block', 'color': '#4ADE80', 'fontSize': '0.75rem', 'fontFamily': 'monospace'}
                        ),
                    ], className="mb-4"),
                    
                    html.Div([
                        html.H6("2. Election Health Score (EHS)™", style={'fontWeight': '600', 'color': '#60A5FA'}),
                        html.P("Calculated programmatically to determine regional administrative stability index:", style={'fontSize': '0.8rem', 'color': '#94A3B8'}),
                        html.Code(
                            "EHS = 0.4*Turnout + 0.2*Awareness + 0.15*Accessibility + 0.15*MomentumFactor - 0.1*RiskPenalty",
                            style={'backgroundColor': '#0F1626', 'padding': '0.5rem 1rem', 'borderRadius': '4px', 'display': 'block', 'color': '#4ADE80', 'fontSize': '0.75rem', 'fontFamily': 'monospace'}
                        ),
                        html.Ul([
                            html.Li("MomentumFactor: Accelerating=100 | Stable=75 | Declining=50", style={'fontSize': '0.75rem', 'marginTop': '0.3rem', 'color': '#94A3B8'}),
                            html.Li("RiskPenalty: High=100 | Medium=50 | Low=0", style={'fontSize': '0.75rem', 'color': '#94A3B8'})
                        ], className="ps-3 mt-1")
                    ], className="mb-4"),
                    
                    html.Div([
                        html.H6("3. Civic Impact Score™", style={'fontWeight': '600', 'color': '#60A5FA'}),
                        html.P("Proprietary indicator combining infrastructure access and localized campaigning parameters:", style={'fontSize': '0.8rem', 'color': '#94A3B8'}),
                        html.Code(
                            "CIS = 0.45*Turnout + 0.25*Awareness + 0.20*Accessibility + 0.10*MomentumFactor",
                            style={'backgroundColor': '#0F1626', 'padding': '0.5rem 1rem', 'borderRadius': '4px', 'display': 'block', 'color': '#4ADE80', 'fontSize': '0.75rem', 'fontFamily': 'monospace'}
                        )
                    ], className="mb-4"),
                    
                    html.Div([
                        html.H6("4. Youth Participation Index™", style={'fontWeight': '600', 'color': '#60A5FA'}),
                        html.P("Modeled to reflect youth demographics engagement relative to awareness outreach metrics:", style={'fontSize': '0.8rem', 'color': '#94A3B8'}),
                        html.Code(
                            "YPI = Average_Youth_Turnout = Final_Turnout * 0.91 * (Awareness_Score / 72.0)",
                            style={'backgroundColor': '#0F1626', 'padding': '0.5rem 1rem', 'borderRadius': '4px', 'display': 'block', 'color': '#4ADE80', 'fontSize': '0.75rem', 'fontFamily': 'monospace'}
                        )
                    ])
                ], className="stat-card p-4 mb-4")
            ], lg=6, md=12),
            
            # Right: ML Stack & Disclosure
            dbc.Col([
                dbc.Card([
                    html.H5("Machine Learning Pipelines", className="mb-4", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
                    
                    html.Div([
                        html.H6("Explainable AI (XAI) feature importance drivers", style={'fontWeight': '600', 'color': '#60A5FA'}),
                        html.P("Each prediction isolates demographic, transport access, holiday drag, and weather comfort features. It calculates exact positive/negative contributions to show why the AI model predicted specific final turnout percentages.", style={'fontSize': '0.8rem', 'color': '#94A3B8'}),
                    ], className="mb-3"),
                    
                    html.Div([
                        html.H6("Random Forest Algorithms", style={'fontWeight': '600', 'color': '#60A5FA'}),
                        html.P("Regression models forecast turnout percentages while Classification models categorize risk levels into Low, Medium, and High risk classifications.", style={'fontSize': '0.8rem', 'color': '#94A3B8'}),
                    ], className="mb-4"),
                    
                    html.H6("Technical Stack Modules", style={'fontWeight': '600', 'color': '#F8FAFC', 'marginBottom': '0.6rem'}),
                    html.Ul([
                        html.Li("Python 3.13.9: Core program architecture & pandas ETL pipelines.", style={'fontSize': '0.8rem', 'color': '#94A3B8', 'marginBottom': '0.2rem'}),
                        html.Li("Dash & Bootstrap Components: Interactive UI layouts and HTML wrappers.", style={'fontSize': '0.8rem', 'color': '#94A3B8', 'marginBottom': '0.2rem'}),
                        html.Li("Plotly: Dynamic responsive chart drawing engines.", style={'fontSize': '0.8rem', 'color': '#94A3B8', 'marginBottom': '0.2rem'}),
                        html.Li("Scikit-Learn & Joblib: ML model fitting, evaluation, and serialization.", style={'fontSize': '0.8rem', 'color': '#94A3B8'})
                    ], className="ps-3 mb-4"),
                    
                    # Ethical disclosure banner
                    html.Div([
                        html.Div("Academic Civic-Tech Disclaimer", style={'fontWeight': '700', 'color': '#EF4444', 'fontSize': '0.85rem', 'marginBottom': '0.4rem'}),
                        html.P(
                            "This dashboard represents an academic simulation application. It does not represent, predict, or casting official election results for the Election Commission of India. All metrics, calculations, model outcomes, and geographic structures are generated synthetically for academic demonstration, auditing, and analytics evaluation purposes.",
                            style={'fontSize': '0.75rem', 'color': '#FCA5A5', 'margin': 0, 'lineHeight': '1.3'}
                        )
                    ], className="custom-alert p-3 rounded active-pulse", style={'border': '1px solid rgba(239, 68, 68, 0.3)'})
                ], className="stat-card p-4")
            ], lg=6, md=12)
        ]),
        
        # Comparative Matrix card
        dbc.Card([
            html.H5("System Comparison Matrix", className="mb-3", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
            html.P("How VoteVision AI compares to standard descriptive dashboards used in election reports:", style={'fontSize': '0.85rem', 'color': '#94A3B8'}),
            comparative_table
        ], className="stat-card p-4 mb-4")
    ])
