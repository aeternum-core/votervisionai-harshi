import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
TRAINED_MODELS_DIR = os.path.join(MODELS_DIR, 'trained')

# Make sure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(TRAINED_MODELS_DIR, exist_ok=True)

# File Paths
DATASET_PATH = os.path.join(DATA_DIR, 'election_data.csv')
TURNOUT_MODEL_PATH = os.path.join(TRAINED_MODELS_DIR, 'turnout_model.pkl')
RISK_MODEL_PATH = os.path.join(TRAINED_MODELS_DIR, 'risk_model.pkl')

# UI Styling Configuration (Command Center Theme)
COLOR_PALETTE = {
    'bg_main': '#0B1220',         # Dark Slate Navy
    'bg_card': '#151F32',         # Light Slate Card
    'primary': '#2563EB',         # Accent Cyber Blue
    'success': '#22C55E',         # Glowing Green (Low Risk, High Turnout)
    'warning': '#FACC15',         # Cyber Yellow/Gold (Medium Risk)
    'danger': '#EF4444',          # Neon Red (High Risk, Alerts)
    'info': '#06B6D4',            # Cyan
    'text_primary': '#F8FAFC',    # Off White
    'text_secondary': '#94A3B8',  # Gray-Blue Accent
    'border': '#1E293B',          # Border Gray
    'glow': 'rgba(37, 99, 235, 0.15)'
}

# Regional Multilingual Support Interface Options
LANGUAGES = {
    'en': {
        'title': 'VoteVision AI',
        'subtitle': 'AI-Powered Smart Election Intelligence Dashboard',
        'tagline': 'Predicting Participation. Empowering Democracy.',
        'command_center': 'Command Center',
        'live_turnout': 'Live Turnout',
        'prediction_center': 'Prediction Center',
        'risk_intel': 'Risk Intelligence',
        'what_if': 'What-If Simulator',
        'recommendations': 'Strategy Advisor',
        'admin_panel': 'Admin & Data',
        'about': 'About Platform'
    },
    'hi': {
        'title': 'मतदृष्टि एआई',
        'subtitle': 'एआई-संचालित स्मार्ट चुनाव खुफिया डैशबोर्ड',
        'tagline': 'भागीदारी का पूर्वानुमान। लोकतंत्र का सशक्तिकरण।',
        'command_center': 'कमांड सेंटर',
        'live_turnout': 'लाइव मतदान',
        'prediction_center': 'पूर्वानुमान केंद्र',
        'risk_intel': 'जोखिम इंटेलिजेंस',
        'what_if': 'व्हाट-इफ सिमुलेटर',
        'recommendations': 'रणनीति सलाहकार',
        'admin_panel': 'एडमिन और डेटा',
        'about': 'मंच के बारे में'
    },
    'kn': {
        'title': 'ಮತವಿಷನ್ ಎಐ',
        'subtitle': 'ಎಐ-ಚಾಲಿತ ಸ್ಮಾರ್ಟ್ ಚುನಾವಣಾ ಗುಪ್ತಚರ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್',
        'tagline': 'ಭಾಗವಹಿಸುವಿಕೆಯ ಮುನ್ಸೂಚನೆ. ಪ್ರಜಾಪ್ರಭುತ್ವದ ಸಬಲೀಕರಣ.',
        'command_center': 'ನಿಯಂತ್ರಣ ಕೊಠಡಿ',
        'live_turnout': 'ಲೈವ್ ಮತದಾನ',
        'prediction_center': 'ಮುನ್ಸೂಚನಾ ಕೇಂದ್ರ',
        'risk_intel': 'ಅಪಾಯ ವಿಶ್ಲೇಷಣೆ',
        'what_if': 'ವಾಟ್-ಇಫ್ ಸಿಮ್ಯುಲೇಟರ್',
        'recommendations': 'ಕಾರ್ಯತಂತ್ರ ಸಲಹೆಗಾರ',
        'admin_panel': 'ನಿರ್ವಹಣೆ ಮತ್ತು ಡೇಟಾ',
        'about': 'ವೇದಿಕೆಯ ಬಗ್ಗೆ'
    }
}
