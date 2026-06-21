from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import sys
import os
import io
import base64
import json

# Ensure parent directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import config
from services.data_service import DataService
from data.synthetic_generator import generate_synthetic_data
from models.turnout_model import train_and_save_models

data_service = DataService()

def get_layout(lang='en'):
    # Load evaluation metrics
    eval_metrics = data_service.model_eval
    
    reg_metrics = []
    clf_metrics = []
    
    if eval_metrics:
        if 'regression' in eval_metrics:
            r = eval_metrics['regression']
            reg_metrics = [
                html.P([html.Strong("Mean Absolute Error (MAE): "), f"{r['mae']:.4f}"]),
                html.P([html.Strong("Root Mean Squared Error (RMSE): "), f"{r['rmse']:.4f}"]),
                html.P([html.Strong("R-squared (R² Score): "), f"{r['r2']:.4f}"]),
            ]
        if 'classification' in eval_metrics:
            c = eval_metrics['classification']
            clf_metrics = [
                html.P([html.Strong("Overall Accuracy: "), f"{c['accuracy']*100:.2f}%"]),
                html.P([html.Strong("Precision: "), f"{c['precision']:.4f}"]),
                html.P([html.Strong("Recall: "), f"{c['recall']:.4f}"]),
                html.P([html.Strong("F1-Score: "), f"{c['f1_score']:.4f}"]),
            ]
    else:
        reg_metrics = [html.P("No model training records found. Retrain model below.")]
        clf_metrics = [html.P("No model training records found. Retrain model below.")]
        
    return html.Div([
        # Title
        html.Div([
            html.H3("Admin & Data Management Center", style={'fontFamily': 'Poppins', 'fontWeight': '600', 'color': '#F8FAFC'}),
            html.P("Upload local constituency datasets, trigger synthetic engine recalibration, and audit AI classification parameters.", style={'color': '#94A3B8'})
        ], className="mb-4"),
        
        dbc.Row([
            # Data operations
            dbc.Col([
                dbc.Card([
                    html.H5("Voter Data Ingestion", className="mb-4", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
                    
                    # CSV upload
                    html.Label("Upload Custom Election CSV", className="form-label-custom"),
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select CSV File', style={'color': '#60A5FA', 'fontWeight': '600'})
                        ]),
                        style={
                            'width': '100%',
                            'height': '80px',
                            'lineHeight': '80px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '8px',
                            'borderColor': '#1E293B',
                            'textAlign': 'center',
                            'backgroundColor': '#0F1626',
                            'color': '#94A3B8',
                            'cursor': 'pointer'
                        },
                        multiple=False,
                        className="mb-4"
                    ),
                    
                    html.Div(id='upload-alert-container'),
                    
                    html.Label("Demographic Data Synthesizer", className="form-label-custom"),
                    html.P("Re-generate standard Indian geographic synthetic dataset (15 states, 171 constituencies).", style={'fontSize': '0.8rem', 'color': '#94A3B8'}),
                    dbc.Button("Generate Synthetic Data", id='gen-data-btn', color="secondary", className="w-100 mb-3"),
                    html.Div(id='gen-alert-container'),
                    
                    html.Label("Model Pipeline Controls", className="form-label-custom"),
                    html.P("Retrain Random Forest Regressor & Classifier models based on current CSV dataset.", style={'fontSize': '0.8rem', 'color': '#94A3B8'}),
                    dbc.Button("Re-Train AI Models", id='train-models-btn', color="primary", className="w-100"),
                    html.Div(id='train-alert-container', className="mt-3")
                ], className="stat-card p-4 h-100")
            ], lg=6, md=12, className="mb-4"),
            
            # Model metrics
            dbc.Col([
                dbc.Card([
                    html.H5("AI Core Validation Auditing", className="mb-4", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
                    
                    html.Label("Final Turnout Predictor (Regression)", className="form-label-custom"),
                    html.Div(reg_metrics, className="p-3 mb-4 rounded border border-secondary", style={'backgroundColor': '#0F1626', 'fontSize': '0.85rem'}),
                    
                    html.Label("Turnout Risk Classifier (Classification)", className="form-label-custom"),
                    html.Div(clf_metrics, className="p-3 mb-4 rounded border border-secondary", style={'backgroundColor': '#0F1626', 'fontSize': '0.85rem'}),
                    
                    html.Label("Database Storage Information", className="form-label-custom"),
                    html.Div([
                        html.P([html.Strong("Storage Location: "), f"{config.DATASET_PATH} (Local flat CSV Data Service Layer)"]),
                        html.P([html.Strong("Data Shape: "), f"{len(data_service.df) if not data_service.df.empty else 0} records × 27 columns"])
                    ], className="p-3 rounded border border-secondary", style={'backgroundColor': '#0F1626', 'fontSize': '0.85rem'})
                ], className="stat-card p-4 h-100")
            ], lg=6, md=12, className="mb-4")
        ])
    ])

# Callback for CSV Upload Ingestion
@callback(
    Output('upload-alert-container', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    prevent_initial_call=True
)
def handle_csv_upload(contents, filename):
    if contents is None:
        return None
        
    try:
        # Parse content
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        # Read into dataframe
        df_upload = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        
        # Required validation columns
        required_cols = [
            'state', 'district', 'constituency', 'region_type', 'population',
            'registered_voters', 'male_voters', 'female_voters', 'youth_voters',
            'senior_voters', 'literacy_rate', 'transport_accessibility', 'awareness_score',
            'weather_score', 'campaign_intensity', 'holiday_factor', 'historical_turnout',
            'current_turnout', 'participation_momentum', 'risk_level', 'actual_final_turnout'
        ]
        
        missing = [col for col in required_cols if col not in df_upload.columns]
        if missing:
            return dbc.Alert(f"Upload failed. Missing required columns: {', '.join(missing)}", color="danger", dismissable=True)
            
        # Save to main path
        df_upload.to_csv(config.DATASET_PATH, index=False)
        data_service.load_data() # Reload data service
        
        return dbc.Alert(f"File '{filename}' uploaded successfully! Ingested {len(df_upload)} records.", color="success", dismissable=True)
    except Exception as e:
        return dbc.Alert(f"Error parsing file: {str(e)}", color="danger", dismissable=True)

# Callback to generate synthetic data
@callback(
    Output('gen-alert-container', 'children'),
    Input('gen-data-btn', 'n_clicks'),
    prevent_initial_call=True
)
def handle_generate_data(n_clicks):
    try:
        generate_synthetic_data()
        data_service.load_data() # Reload in memory
        return dbc.Alert("Synthetic dataset generated and loaded successfully!", color="success", dismissable=True)
    except Exception as e:
        return dbc.Alert(f"Generation failed: {str(e)}", color="danger", dismissable=True)

# Callback to train models
@callback(
    Output('train-alert-container', 'children'),
    Input('train-models-btn', 'n_clicks'),
    prevent_initial_call=True
)
def handle_train_models(n_clicks):
    try:
        train_and_save_models()
        data_service.load_models() # Reload in memory
        return dbc.Alert("ML models trained and saved to program files successfully!", color="success", dismissable=True)
    except Exception as e:
        return dbc.Alert(f"Training failed: {str(e)}", color="danger", dismissable=True)
