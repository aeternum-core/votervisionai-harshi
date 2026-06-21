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

PAGE_TRANSLATIONS = {
    'en': {
        'title': "Admin & Data Management Center",
        'subtitle': "Upload local constituency datasets, trigger synthetic engine recalibration, and audit AI classification parameters.",
        'ingestion_header': "Voter Data Ingestion",
        'upload_label': "Upload Custom Election CSV",
        'upload_drag': "Drag and Drop or ",
        'upload_select': "Select CSV File",
        'synthesizer_label': "Demographic Data Synthesizer",
        'synthesizer_desc': "Re-generate standard Indian geographic synthetic dataset (15 states, 171 constituencies).",
        'btn_gen_data': "Generate Synthetic Data",
        'pipeline_label': "Model Pipeline Controls",
        'pipeline_desc': "Retrain Random Forest Regressor & Classifier models based on current CSV dataset.",
        'btn_train': "Re-Train AI Models",
        'auditing_header': "AI Core Validation Auditing",
        'regression_label': "Final Turnout Predictor (Regression)",
        'classification_label': "Turnout Risk Classifier (Classification)",
        'storage_label': "Database Storage Information",
        'storage_loc': "Storage Location",
        'storage_shape': "Data Shape",
        'no_records': "No model training records found. Retrain model below.",
        'records_text': "records × 27 columns",
        'local_storage_info': "Local flat CSV Data Service Layer",
        'mae': "Mean Absolute Error (MAE)",
        'rmse': "Root Mean Squared Error (RMSE)",
        'r2': "R-squared (R² Score)",
        'accuracy': "Overall Accuracy",
        'precision': "Precision",
        'recall': "Recall",
        'f1': "F1-Score",
        
        # Alerts
        'alert_upload_fail': "Upload failed. Missing required columns: {cols}",
        'alert_upload_success': "File '{filename}' uploaded successfully! Ingested {count} records.",
        'alert_upload_error': "Error parsing file: {err}",
        'alert_gen_success': "Synthetic dataset generated and loaded successfully!",
        'alert_gen_fail': "Generation failed: {err}",
        'alert_train_success': "ML models trained and saved to program files successfully!",
        'alert_train_fail': "Training failed: {err}"
    },
    'hi': {
        'title': "एडमिन और डेटा प्रबंधन केंद्र",
        'subtitle': "स्थानीय निर्वाचन क्षेत्र डेटासेट अपलोड करें, सिंथेटिक इंजन रीकैलिब्रेशन ट्रिगर करें, और एआई वर्गीकरण मापदंडों का ऑडिट करें।",
        'ingestion_header': "मतदाता डेटा अंतर्ग्रहण (Ingestion)",
        'upload_label': "कस्टम चुनाव CSV अपलोड करें",
        'upload_drag': "ड्रैग और ड्रॉप करें या ",
        'upload_select': "CSV फ़ाइल चुनें",
        'synthesizer_label': "जनसांख्यिकी डेटा सिंथेसाइज़र",
        'synthesizer_desc': "मानक भारतीय भौगोलिक सिंथेटिक डेटासेट (15 राज्य, 171 निर्वाचन क्षेत्र) को फिर से उत्पन्न करें।",
        'btn_gen_data': "सिंथेटिक डेटा उत्पन्न करें",
        'pipeline_label': "मॉडल पाइपलाइन नियंत्रण",
        'pipeline_desc': "वर्तमान CSV डेटासेट के आधार पर रैंडम फॉरेस्ट रिग्रेसर और क्लासिफायर मॉडल को फिर से प्रशिक्षित करें।",
        'btn_train': "एआई मॉडल को फिर से प्रशिक्षित करें",
        'auditing_header': "एआई कोर सत्यापन ऑडिटिंग",
        'regression_label': "अंतिम मतदान पूर्वानुमानक (Regression)",
        'classification_label': "मतदान जोखिम क्लासिफायर (Classification)",
        'storage_label': "डेटाबेस स्टोरेज जानकारी",
        'storage_loc': "भंडारण स्थान",
        'storage_shape': "डेटा संरचना",
        'no_records': "कोई मॉडल प्रशिक्षण रिकॉर्ड नहीं मिला। नीचे मॉडल को फिर से प्रशिक्षित करें।",
        'records_text': "रिकॉर्ड × 27 कॉलम",
        'local_storage_info': "स्थानीय फ्लैट CSV डेटा सेवा परत",
        'mae': "माध्य पूर्ण त्रुटि (MAE)",
        'rmse': "मूल माध्य वर्ग त्रुटि (RMSE)",
        'r2': "आर-वर्ग (R² स्कोर)",
        'accuracy': "कुल सटीकता",
        'precision': "परिशुद्धता (Precision)",
        'recall': "रीकॉल (Recall)",
        'f1': "F1-स्कोर",
        
        # Alerts
        'alert_upload_fail': "अपलोड विफल रहा। आवश्यक कॉलम अनुपस्थित हैं: {cols}",
        'alert_upload_success': "फ़ाइल '{filename}' सफलतापूर्वक अपलोड की गई! {count} रिकॉर्ड आयात किए गए।",
        'alert_upload_error': "फ़ाइल पार्स करने में त्रुटि: {err}",
        'alert_gen_success': "सिंथेटिक डेटासेट सफलतापूर्वक उत्पन्न और लोड किया गया!",
        'alert_gen_fail': "पीढ़ी विफल रही: {err}",
        'alert_train_success': "एआई मॉडल सफलतापूर्वक प्रशिक्षित और प्रोग्राम फाइलों में सहेजे गए!",
        'alert_train_fail': "प्रशिक्षण विफल रहा: {err}"
    },
    'kn': {
        'title': "ನಿರ್ವಹಣೆ ಮತ್ತು ಡೇಟಾ ನಿರ್ವಹಣಾ ಕೇಂದ್ರ",
        'subtitle': "ಸ್ಥಳೀಯ ಮತಕ್ಷೇತ್ರದ ಡೇಟಾಸೆಟ್‌ಗಳನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ, ಸಿಂಥೆಟಿಕ್ ಎಂಜಿನ್ ಮರುಮಾಪನವನ್ನು ಸಕ್ರಿಯಗೊಳಿಸಿ ಮತ್ತು ಎಐ ವರ್ಗೀಕರಣ ನಿಯತಾಂಕಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.",
        'ingestion_header': "ಮತದಾರರ ಡೇಟಾ ಇಂಗೇಸ್ಷನ್",
        'upload_label': "ಕಸ್ಟಮ್ ಚುನಾವಣಾ CSV ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        'upload_drag': "ಡ್ರ್ಯಾಗ್ ಮತ್ತು ಡ್ರಾಪ್ ಮಾಡಿ ಅಥವಾ ",
        'upload_select': "CSV ಫೈಲ್ ಆಯ್ಕೆಮಾಡಿ",
        'synthesizer_label': "ಜನಸಂಖ್ಯಾ ಡೇಟಾ ಸಿಂಥೆಸೈಜರ್",
        'synthesizer_desc': "ಸಾಮಾನ್ಯ ಭಾರತೀಯ ಭೌಗೋಳಿಕ ಸಿಂಥೆಟಿಕ್ ಡೇಟಾಸೆಟ್ (15 ರಾಜ್ಯಗಳು, 171 ಮತಕ್ಷೇತ್ರಗಳು) ಅನ್ನು ಮರು-ರಚಿಸಿ.",
        'btn_gen_data': "ಸಿಂಥೆಟಿಕ್ ಡೇಟಾ ರಚಿಸಿ",
        'pipeline_label': "ಮಾದರಿ ಪೈಪ್‌ಲೈನ್ ನಿಯಂತ್ರಣಗಳು",
        'pipeline_desc': "ಪ್ರಸ್ತುತ CSV ಡೇಟಾಸೆಟ್ ಆಧಾರದ ಮೇಲೆ ರಾಂಡಮ್ ಫಾರೆಸ್ಟ್ ರಿಗ್ರೆಸರ್ ಮತ್ತು ಕ್ಲಾಸಿಫೈಯರ್ ಮಾದರಿಗಳನ್ನು ಮರುತರಬೇತಿಗೊಳಿಸಿ.",
        'btn_train': "ಎಐ ಮಾದರಿಗಳಿಗೆ ಮರುತರಬೇತಿ ನೀಡಿ",
        'auditing_header': "ಎಐ ಕೋರ್ ಮೌಲ್ಯಮಾಪನ ಪರಿಶೀಲನೆ",
        'regression_label': "ಅಂತಿಮ ಮತದಾನ ಮುನ್ಸೂಚಕ (Regression)",
        'classification_label': "ಮತದಾನ ಅಪಾಯದ ಕ್ಲಾಸಿಫೈಯರ್ (Classification)",
        'storage_label': "ಡೇಟಾಬೇಸ್ ಸಂಗ್ರಹಣಾ ಮಾಹಿತಿ",
        'storage_loc': "ಸಂಗ್ರಹಣಾ ಸ್ಥಳ",
        'storage_shape': "ಡೇಟಾ ಆಕಾರ",
        'no_records': "ಯಾವುದೇ ಮಾದರಿ ತರಬೇತಿ ದಾಖಲೆಗಳು ಕಂಡುಬಂದಿಲ್ಲ. ಕೆಳಗೆ ಮರುತರಬೇತಿ ನೀಡಿ.",
        'records_text': "ದಾಖಲೆಗಳು × 27 ಕಾಲಮ್‌ಗಳು",
        'local_storage_info': "ಸ್ಥಳೀಯ ಫ್ಲಾಟ್ CSV ಡೇಟಾ ಸೇವಾ ಪದರ",
        'mae': "ಸರಾಸರಿ ಸಂಪೂರ್ಣ ದೋಷ (MAE)",
        'rmse': "ಮೂಲ ಸರಾಸರಿ ವರ್ಗದ ದೋಷ (RMSE)",
        'r2': "ಆರ್-ವರ್ಗ (R² ಸ್ಕೋರ್)",
        'accuracy': "ಒಟ್ಟಾರೆ ನಿಖರತೆ",
        'precision': "ನಿಖರತೆ (Precision)",
        'recall': "ಮರುಸ್ಥಾಪನೆ (Recall)",
        'f1': "ಎಫ್1-ಸ್ಕೋರ್",
        
        # Alerts
        'alert_upload_fail': "ಅಪ್‌ಲೋಡ್ ವಿಫಲವಾಗಿದೆ. ಅಗತ್ಯವಿರುವ ಕಾಲಮ್‌ಗಳು ಕಾಣೆಯಾಗಿವೆ: {cols}",
        'alert_upload_success': "ಫೈಲ್ '{filename}' ಯಶಸ್ವಿಯಾಗಿ ಅಪ್‌ಲೋಡ್ ಆಗಿದೆ! {count} ದಾಖಲೆಗಳನ್ನು ಸೇರಿಸಲಾಗಿದೆ.",
        'alert_upload_error': "ಫೈಲ್ ಪಾರ್ಸ್ ಮಾಡುವಲ್ಲಿ ದೋಷ: {err}",
        'alert_gen_success': "ಸಿಂಥೆಟಿಕ್ ಡೇಟಾಸೆಟ್ ಯಶಸ್ವಿಯಾಗಿ ರಚಿಸಲಾಗಿದೆ ಮತ್ತು ಲೋಡ್ ಆಗಿದೆ!",
        'alert_gen_fail': "ರಚನೆ ವಿಫಲವಾಗಿದೆ: {err}",
        'alert_train_success': "ಎಐ ಮಾದರಿಗಳಿಗೆ ಯಶಸ್ವಿಯಾಗಿ ತರಬೇತಿ ನೀಡಲಾಗಿದೆ ಮತ್ತು ಫೈಲ್ ಸೇವ್ ಆಗಿದೆ!",
        'alert_train_fail': "ತರಬೇತಿ ವಿಫಲವಾಗಿದೆ: {err}"
    }
}

def get_layout(lang='en'):
    t = PAGE_TRANSLATIONS.get(lang, PAGE_TRANSLATIONS['en'])
    # Load evaluation metrics
    eval_metrics = data_service.model_eval
    
    reg_metrics = []
    clf_metrics = []
    
    if eval_metrics:
        if 'regression' in eval_metrics:
            r = eval_metrics['regression']
            reg_metrics = [
                html.P([html.Strong(f"{t['mae']}: "), f"{r['mae']:.4f}"]),
                html.P([html.Strong(f"{t['rmse']}: "), f"{r['rmse']:.4f}"]),
                html.P([html.Strong(f"{t['r2']}: "), f"{r['r2']:.4f}"]),
            ]
        if 'classification' in eval_metrics:
            c = eval_metrics['classification']
            clf_metrics = [
                html.P([html.Strong(f"{t['accuracy']}: "), f"{c['accuracy']*100:.2f}%"]),
                html.P([html.Strong(f"{t['precision']}: "), f"{c['precision']:.4f}"]),
                html.P([html.Strong(f"{t['recall']}: "), f"{c['recall']:.4f}"]),
                html.P([html.Strong(f"{t['f1']}: "), f"{c['f1_score']:.4f}"]),
            ]
    else:
        reg_metrics = [html.P(t['no_records'])]
        clf_metrics = [html.P(t['no_records'])]
        
    return html.Div([
        # Title
        html.Div([
            html.H3(t['title'], style={'fontFamily': 'Poppins', 'fontWeight': '600', 'color': '#F8FAFC'}),
            html.P(t['subtitle'], style={'color': '#94A3B8'})
        ], className="mb-4"),
        
        dbc.Row([
            # Data operations
            dbc.Col([
                dbc.Card([
                    html.H5(t['ingestion_header'], className="mb-4", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
                    
                    # CSV upload
                    html.Label(t['upload_label'], className="form-label-custom"),
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            t['upload_drag'],
                            html.A(t['upload_select'], style={'color': '#60A5FA', 'fontWeight': '600'})
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
                    
                    html.Label(t['synthesizer_label'], className="form-label-custom"),
                    html.P(t['synthesizer_desc'], style={'fontSize': '0.8rem', 'color': '#94A3B8'}),
                    dbc.Button(t['btn_gen_data'], id='gen-data-btn', color="secondary", className="w-100 mb-3"),
                    html.Div(id='gen-alert-container'),
                    
                    html.Label(t['pipeline_label'], className="form-label-custom"),
                    html.P(t['pipeline_desc'], style={'fontSize': '0.8rem', 'color': '#94A3B8'}),
                    dbc.Button(t['btn_train'], id='train-models-btn', color="primary", className="w-100"),
                    html.Div(id='train-alert-container', className="mt-3")
                ], className="stat-card p-4 h-100")
            ], lg=6, md=12, className="mb-4"),
            
            # Model metrics
            dbc.Col([
                dbc.Card([
                    html.H5(t['auditing_header'], className="mb-4", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
                    
                    html.Label(t['regression_label'], className="form-label-custom"),
                    html.Div(reg_metrics, className="audit-box p-3 mb-4 rounded border border-secondary", style={'backgroundColor': '#0F1626', 'fontSize': '0.85rem', 'color': '#F8FAFC'}),
                    
                    html.Label(t['classification_label'], className="form-label-custom"),
                    html.Div(clf_metrics, className="audit-box p-3 mb-4 rounded border border-secondary", style={'backgroundColor': '#0F1626', 'fontSize': '0.85rem', 'color': '#F8FAFC'}),
                    
                    html.Label(t['storage_label'], className="form-label-custom"),
                    html.Div([
                        html.P([html.Strong(f"{t['storage_loc']}: "), f"data/election_data.csv ({t['local_storage_info']})"]),
                        html.P([html.Strong(f"{t['storage_shape']}: "), f"{len(data_service.df) if not data_service.df.empty else 0} {t['records_text']}"])
                    ], className="audit-box p-3 rounded border border-secondary", style={'backgroundColor': '#0F1626', 'fontSize': '0.85rem', 'color': '#F8FAFC'})
                ], className="stat-card p-4 h-100")
            ], lg=6, md=12, className="mb-4")
        ])
    ])

# Callback for CSV Upload Ingestion
@callback(
    Output('upload-alert-container', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('lang-store', 'data'),
    prevent_initial_call=True
)
def handle_csv_upload(contents, filename, lang):
    if not lang:
        lang = 'en'
    t = PAGE_TRANSLATIONS.get(lang, PAGE_TRANSLATIONS['en'])

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
            return dbc.Alert(t['alert_upload_fail'].format(cols=', '.join(missing)), color="danger", dismissable=True)
            
        # Save to main path
        df_upload.to_csv(config.DATASET_PATH, index=False)
        data_service.load_data() # Reload data service
        
        return dbc.Alert(t['alert_upload_success'].format(filename=filename, count=len(df_upload)), color="success", dismissable=True)
    except Exception as e:
        return dbc.Alert(t['alert_upload_error'].format(err=str(e)), color="danger", dismissable=True)

# Callback to generate synthetic data
@callback(
    Output('gen-alert-container', 'children'),
    Input('gen-data-btn', 'n_clicks'),
    State('lang-store', 'data'),
    prevent_initial_call=True
)
def handle_generate_data(n_clicks, lang):
    if not lang:
        lang = 'en'
    t = PAGE_TRANSLATIONS.get(lang, PAGE_TRANSLATIONS['en'])

    try:
        generate_synthetic_data()
        data_service.load_data() # Reload in memory
        return dbc.Alert(t['alert_gen_success'], color="success", dismissable=True)
    except Exception as e:
        return dbc.Alert(t['alert_gen_fail'].format(err=str(e)), color="danger", dismissable=True)

# Callback to train models
@callback(
    Output('train-alert-container', 'children'),
    Input('train-models-btn', 'n_clicks'),
    State('lang-store', 'data'),
    prevent_initial_call=True
)
def handle_train_models(n_clicks, lang):
    if not lang:
        lang = 'en'
    t = PAGE_TRANSLATIONS.get(lang, PAGE_TRANSLATIONS['en'])

    try:
        train_and_save_models()
        data_service.load_models() # Reload in memory
        return dbc.Alert(t['alert_train_success'], color="success", dismissable=True)
    except Exception as e:
        return dbc.Alert(t['alert_train_fail'].format(err=str(e)), color="danger", dismissable=True)
