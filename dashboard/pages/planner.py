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

PAGE_TRANSLATIONS = {
    'en': {
        'title': "Election Strategy Advisor™",
        'subtitle': "Access prescriptive strategy actions mapped to specific regional voter participation barriers to systematically boost democracy.",
        'select_state': "Select Target State",
        'priority_threshold': "Intervention Priority Threshold",
        'threshold_high': "High Priority (Priority Index > 15)",
        'threshold_all': "Show All Needs",
        'all_states': "All States",
        'methodology_header': "Election Strategy Advisor™ Prescriptions",
        'methodology_desc': "Our AI evaluates live socio-economic deficits and polling progression to recommend targeted voter turnout recovery plans:",
        'methodology_1': "If accessibility scores are low -> deploy polling station transport shuttles.",
        'methodology_2': "If youth demographics are high but turnout is low -> launch targeted social media micro-campaigns.",
        'methodology_3': "If weather scores are under 50 -> set up heat/rain queue canopies and water kiosks.",
        'methodology_4': "If overall awareness is low -> deploy door-to-door volunteers and local language audio boards.",
        'queue_header': "Ranked Strategic Interventions Queue",
        'btn_export': "Export Strategy Report (CSV)",
        'no_intervention': "No areas require urgent intervention.",
        'no_match_priority': "No active areas match high priority criteria (Priority Index > 15).",
        'lbl_strategic_rank': "STRATEGIC RANK",
        'lbl_priority_index': "Priority Index",
        'lbl_early_turnout': "Early Turnout",
        'lbl_historical_target': "Historical Target",
        'lbl_risk_rating': "Risk Rating",
        'lbl_diagnosed_barrier': "Diagnosed Barrier: ",
        'lbl_prescriptive_actions': "PRESCRIPTIVE ACTION RECIPES",
        'lbl_expected_gain': "Expected Gain",
        'lbl_difficulty': "Difficulty",
        'high': "High",
        'medium': "Medium",
        'low': "Low",
        'easy': "Easy"
    },
    'hi': {
        'title': "चुनाव रणनीति सलाहकार™",
        'subtitle': "लोकतंत्र को व्यवस्थित रूप से बढ़ावा देने के लिए विशिष्ट क्षेत्रीय मतदाता भागीदारी बाधाओं के लिए निर्धारित रणनीतिक कार्यों तक पहुंचें।",
        'select_state': "लक्षित राज्य चुनें",
        'priority_threshold': "हस्तक्षेप प्राथमिकता सीमा",
        'threshold_high': "उच्च प्राथमिकता (प्राथमिकता सूचकांक > 15)",
        'threshold_all': "सभी आवश्यकताएं दिखाएं",
        'all_states': "सभी राज्य",
        'methodology_header': "चुनाव रणनीति सलाहकार™ नुस्खे",
        'methodology_desc': "हमारा एआई लक्षित मतदाता मतदान सुधार योजनाओं की सिफारिश करने के लिए लाइव सामाजिक-आर्थिक घाटे और मतदान प्रगति का मूल्यांकन करता है:",
        'methodology_1': "यदि सुलभता स्कोर कम है -> मतदान केंद्र परिवहन शटल तैनात करें।",
        'methodology_2': "यदि युवा जनसांख्यिकी उच्च है लेकिन मतदान कम है -> लक्षित सोशल मीडिया माइक्रो-अभियान शुरू करें।",
        'methodology_3': "यदि मौसम का स्कोर 50 से कम है -> हीट/बारिश कतार कैनोपी और पानी के कियोस्क स्थापित करें।",
        'methodology_4': "यदि समग्र जागरूकता कम है -> घर-घर जाने वाले स्वयंसेवकों और स्थानीय भाषा के ऑडियो बोर्डों को तैनात करें।",
        'queue_header': "रैंक की गई रणनीतिक हस्तक्षेप कतार",
        'btn_export': "रणनीति रिपोर्ट निर्यात करें (CSV)",
        'no_intervention': "किसी भी क्षेत्र में तत्काल हस्तक्षेप की आवश्यकता नहीं है।",
        'no_match_priority': "कोई भी सक्रिय क्षेत्र उच्च प्राथमिकता मानदंडों (प्राथमिकता सूचकांक > 15) से मेल नहीं खाता है।",
        'lbl_strategic_rank': "रणनीतिक रैंक",
        'lbl_priority_index': "प्राथमिकता सूचकांक",
        'lbl_early_turnout': "प्रारंभिक मतदान",
        'lbl_historical_target': "ऐतिहासिक लक्ष्य",
        'lbl_risk_rating': "जोखिम रेटिंग",
        'lbl_diagnosed_barrier': "निदान की गई बाधा: ",
        'lbl_prescriptive_actions': "निर्धारित कार्रवाई विधियां",
        'lbl_expected_gain': "अपेक्षित लाभ",
        'lbl_difficulty': "कठिनाई",
        'high': "उच्च",
        'medium': "मध्यम",
        'low': "निम्न",
        'easy': "आसान"
    },
    'kn': {
        'title': "ಚುನಾವಣಾ ಕಾರ್ಯತಂತ್ರ ಸಲಹೆಗಾರ™",
        'subtitle': "ಪ್ರಜಾಪ್ರಭುತ್ವವನ್ನು ವ್ಯವಸ್ಥಿತವಾಗಿ ಉತ್ತೇಜಿಸಲು ನಿರ್ದಿಷ್ಟ ಪ್ರಾದೇಶಿಕ ಮತದಾರರ ಭಾಗವಹಿಸುವಿಕೆಯ ಅಡಚಣೆಗಳಿಗೆ ಅನುಗುಣವಾಗಿ ಸೂಚಿಸಲಾದ ಕಾರ್ಯತಂತ್ರದ ಕ್ರಮಗಳನ್ನು ಪ್ರವೇಶಿಸಿ.",
        'select_state': "ಗುರಿ ರಾಜ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        'priority_threshold': "ಹಸ್ತಕ್ಷೇಪದ ಆದ್ಯತೆಯ ಮಿತಿ",
        'threshold_high': "ಹೆಚ್ಚಿನ ಆದ್ಯತೆ (ಆದ್ಯತೆಯ ಸೂಚ್ಯಂಕ > 15)",
        'threshold_all': "ಎಲ್ಲಾ ಅಗತ್ಯಗಳನ್ನು ತೋರಿಸು",
        'all_states': "ಎಲ್ಲಾ ರಾಜ್ಯಗಳು",
        'methodology_header': "ಚುನಾವಣಾ ಕಾರ್ಯತಂತ್ರ ಸಲಹೆಗಾರ™ ಶಿಫಾರಸುಗಳು",
        'methodology_desc': "ಲಕ್ಷ್ಯದ ಮತದಾರರ ಮತದಾನ ಮರುಪಡೆಯುವಿಕೆ ಯೋಜನೆಗಳನ್ನು ಶಿಫಾರಸು ಮಾಡಲು ನಮ್ಮ ಎಐ ನೈಜ-ಸಮಯದ ಸಮಾಜೋ-ಆರ್ಥಿಕ ಕೊರತೆಗಳು ಮತ್ತು ಮತದಾನ ಪ್ರಗತಿಯನ್ನು ಮೌಲ್ಯಮಾಪನ ಮಾಡುತ್ತದೆ:",
        'methodology_1': "ಪ್ರವೇಶದ ಸ್ಕೋರ್‌ಗಳು ಕಡಿಮೆಯಿದ್ದರೆ -> ಮತಗಟ್ಟೆ ಸಾರಿಗೆ ಶಟಲ್‌ಗಳನ್ನು ನಿಯೋಜಿಸಿ.",
        'methodology_2': "ಯುವ ಮತದಾರರು ಹೆಚ್ಚಿದ್ದು ಮತದಾನ ಕಡಿಮೆಯಿದ್ದರೆ -> ಗುರಿಪಡಿಸಿದ ಸಾಮಾಜಿಕ ಮಾಧ್ಯಮ ಪ್ರಚಾರಗಳನ್ನು ಪ್ರಾರಂಭಿಸಿ.",
        'methodology_3': "ಹವಾಮಾನ ಸ್ಕೋರ್‌ಗಳು 50 ಕ್ಕಿಂತ ಕಡಿಮೆಯಿದ್ದರೆ -> ಬಿಸಿಲು/ಮಳೆಯ ನೆರಳಿನ ಸಾಲುಗಳು ಮತ್ತು ನೀರಿನ ಕೇಂದ್ರಗಳನ್ನು ಸ್ಥಾಪಿಸಿ.",
        'methodology_4': "ಒಟ್ಟಾರೆ ಜಾಗೃತಿ ಕಡಿಮೆಯಿದ್ದರೆ -> ಮನೆ-ಮನೆಗೆ ಭೇಟಿ ನೀಡುವ ಸ್ವಯಂಸೇವಕರು ಮತ್ತು ಸ್ಥಳೀಯ ಭಾಷೆಯ ಧ್ವನಿಫಲಕಗಳನ್ನು ನಿಯೋಜಿಸಿ.",
        'queue_header': "ಶ್ರೇಣೀಕೃತ ಕಾರ್ಯತಂತ್ರದ ಹಸ್ತಕ್ಷೇಪಗಳ ಸರತಿ ಸಾಲು",
        'btn_export': "ಕಾರ್ಯತಂತ್ರ ವರದಿಯನ್ನು ರಫ್ತು ಮಾಡಿ (CSV)",
        'no_intervention': "ಯಾವ ಪ್ರದೇಶಕ್ಕೂ ತುರ್ತು ಹಸ್ತಕ್ಷೇಪದ ಅಗತ್ಯವಿಲ್ಲ.",
        'no_match_priority': "ಹೆಚ್ಚಿನ ಆದ್ಯತೆಯ ಮಾನದಂಡಗಳಿಗೆ (ಆದ್ಯತೆಯ ಸೂಚ್ಯಂಕ > 15) ಯಾವುದೇ ಸಕ್ರಿಯ ಪ್ರದೇಶಗಳು ಹೊಂದಿಕೆಯಾಗುತ್ತಿಲ್ಲ.",
        'lbl_strategic_rank': "ಕಾರ್ಯತಂತ್ರದ ಶ್ರೇಣಿ",
        'lbl_priority_index': "ಆದ್ಯತೆಯ ಸೂಚ್ಯಂಕ",
        'lbl_early_turnout': "ಆರಂಭಿಕ ಮತದಾನ",
        'lbl_historical_target': "ಐತಿಹಾಸಿಕ ಗುರಿ",
        'lbl_risk_rating': "ಅಪಾಯದ ರೇಟಿಂಗ್",
        'lbl_diagnosed_barrier': "ಪತ್ತೆಯಾದ ಅಡಚಣೆ: ",
        'lbl_prescriptive_actions': "ಶಿಫಾರಸು ಮಾಡಿದ ಕ್ರಮಗಳು",
        'lbl_expected_gain': "ನಿರೀಕ್ಷಿತ ಲಾಭ",
        'lbl_difficulty': "ಕಠಿಣತೆ",
        'high': "ಹೆಚ್ಚು",
        'medium': "ಮಧ್ಯಮ",
        'low': "ಕಡಿಮೆ",
        'easy': "ಸುಲಭ"
    }
}

def get_layout(lang='en'):
    t = PAGE_TRANSLATIONS.get(lang, PAGE_TRANSLATIONS['en'])
    states = data_service.get_states()
    state_options = [{'label': t['all_states'], 'value': 'ALL'}] + [{'label': s, 'value': s} for s in states]
    
    # Static summary card on intervention methodology
    methods_card = dbc.Card([
        html.H5(t['methodology_header'], className="mb-3", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
        html.P(t['methodology_desc'], style={'fontSize': '0.85rem', 'color': '#94A3B8'}),
        html.Ul([
            html.Li(t['methodology_1'], style={'fontSize': '0.8rem', 'marginBottom': '0.3rem'}),
            html.Li(t['methodology_2'], style={'fontSize': '0.8rem', 'marginBottom': '0.3rem'}),
            html.Li(t['methodology_3'], style={'fontSize': '0.8rem', 'marginBottom': '0.3rem'}),
            html.Li(t['methodology_4'], style={'fontSize': '0.8rem'})
        ], className="ps-3 mb-0")
    ], className="stat-card p-4 h-100")

    return html.Div([
        # Header
        html.Div([
            html.H3(t['title'], style={'fontFamily': 'Poppins', 'fontWeight': '600', 'color': '#F8FAFC'}),
            html.P(t['subtitle'], style={'color': '#94A3B8'})
        ], className="mb-4"),
        
        # Row 1: Filters & Explanation
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.Label(t['select_state'], className="form-label-custom"),
                    dcc.Dropdown(
                        id='plan-state-filter',
                        options=state_options,
                        value='ALL',
                        clearable=False,
                        className="bg-dark text-white border-secondary mb-4"
                    ),
                    html.Label(t['priority_threshold'], className="form-label-custom"),
                    dcc.Dropdown(
                        id='plan-priority-filter',
                        options=[
                            {'label': t['threshold_high'], 'value': 'high'},
                            {'label': t['threshold_all'], 'value': 'all'}
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
            html.H5(t['queue_header'], style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
            dbc.Button(t['btn_export'], id='plan-export-btn', color="primary", size="sm", className="ms-auto", style={'fontWeight': '500'})
        ], className="d-flex align-items-center justify-content-between mb-3"),
        
        # List Container
        html.Div(id='plan-queue-container')
    ])

@callback(
    Output('plan-queue-container', 'children'),
    Input('plan-state-filter', 'value'),
    Input('plan-priority-filter', 'value'),
    State('lang-store', 'data')
)
def update_planner_queue(selected_state, priority_threshold, lang):
    if not lang:
        lang = 'en'
    t = PAGE_TRANSLATIONS.get(lang, PAGE_TRANSLATIONS['en'])

    recommendations = data_service.get_interventions(
        state=selected_state if selected_state != 'ALL' else None,
        limit=25
    )
    
    if not recommendations:
        return html.Div(t['no_intervention'], className="text-muted text-center py-4")
        
    # Apply threshold if requested
    if priority_threshold == 'high':
        recommendations = [r for r in recommendations if r['priority_score'] > 15]
        
    if not recommendations:
        return html.Div(t['no_match_priority'], className="text-muted text-center py-4")
        
    # Dynamic text translation mappings
    translated_problems = {
        "General Voter Apathy": {'en': "General Voter Apathy", 'hi': "सामान्य मतदाता उदासीनता", 'kn': "ಸಾಮಾನ್ಯ ಮತದಾರರ ಉದಾಸೀನತೆ"},
        "Low Civic Awareness": {'en': "Low Civic Awareness", 'hi': "कम नागरिक जागरूकता", 'kn': "ಕಡಿಮೆ ನಾಗರಿಕ ಜಾಗೃತಿ"},
        "Transportation Access Gaps": {'en': "Transportation Access Gaps", 'hi': "परिवहन पहुंच में कमी", 'kn': "ಸಾರಿಗೆ ಪ್ರವೇಶದ ಕೊರತೆ"},
        "Severe Weather Drag": {'en': "Severe Weather Drag", 'hi': "गंभीर मौसम का प्रभाव", 'kn': "ವಿಪರೀತ ಹವಾಮಾನದ ಪ್ರಭಾವ"},
        "Low Youth Engagement": {'en': "Low Youth Engagement", 'hi': "कम युवा जुड़ाव", 'kn': "ಕಡಿಮೆ ಯುವ ಭಾಗವಹಿಸುವಿಕೆ"}
    }
    
    translated_actions = {
        "Deploy Door-to-Door Information Volunteers": {
            'en': "Deploy Door-to-Door Information Volunteers",
            'hi': "घर-घर जाकर जानकारी देने वाले स्वयंसेवकों को तैनात करें",
            'kn': "ಮನೆ-ಮನೆಗೆ ಮಾಹಿತಿ ನೀಡುವ ಸ್ವಯಂಸೇವಕರನ್ನು ನಿಯೋಜಿಸಿ"
        },
        "Deploy Multilingual Audio Van Campaigns": {
            'en': "Deploy Multilingual Audio Van Campaigns",
            'hi': "बहुभाषी ऑडियो वैन अभियान तैनात करें",
            'kn': "ಬಹುಭಾಷಾ ಆಡಿಯೋ ವ್ಯಾನ್ ಪ್ರಚಾರಗಳನ್ನು ನಿಯೋಜಿಸಿ"
        },
        "Deploy Free Polling Station Shuttle Fleet": {
            'en': "Deploy Free Polling Station Shuttle Fleet",
            'hi': "निःशुल्क मतदान केंद्र शटल बेड़े को तैनात करें",
            'kn': "ಉಚಿತ ಮತಗಟ್ಟೆ ಶಟಲ್ ವಾಹನಗಳನ್ನು ನಿಯೋಜಿಸಿ"
        },
        "Erect Cooling Tents, Shaded Queues & Water Stations": {
            'en': "Erect Cooling Tents, Shaded Queues & Water Stations",
            'hi': "कूलिंग टेंट, छायादार कतारें और पानी के स्टेशन स्थापित करें",
            'kn': "ಕೂಲಿಂಗ್ ಟೆಂಟ್ಗಳು, ನೆರಳಿನ ಸಾಲುಗಳು ಮತ್ತು ನೀರಿನ ಕೇಂದ್ರಗಳನ್ನು ಸ್ಥಾಪಿಸಿ"
        },
        "Launch College Campus Rallies & Social Voting Challenges": {
            'en': "Launch College Campus Rallies & Social Voting Challenges",
            'hi': "कॉलेज कैंपस रैलियां और सोशल वोटिंग चुनौतियां शुरू करें",
            'kn': "ಕಾಲೇಜು ಕ್ಯಾಂಪಸ್ ರ್ಯಾಲಿಗಳು ಮತ್ತು ಸಾಮಾಜಿಕ ಮತದಾನ ಸವಾಲುಗಳನ್ನು ಪ್ರಾರಂಭಿಸಿ"
        },
        "Broadcast Localized SMS Broadcast Notifications": {
            'en': "Broadcast Localized SMS Broadcast Notifications",
            'hi': "स्थानीयकृत एसएमएस प्रसारण सूचनाएं प्रसारित करें",
            'kn': "ಸ್ಥಳೀಯ ಎಸ್‌ಎಮ್‌ಎಸ್ ಪ್ರಸಾರ ಅಧಿಸೂಚನೆಗಳನ್ನು ಕಳುಹಿಸಿ"
        },
        "Maintain Standard Voter Pamphlet Distribution": {
            'en': "Maintain Standard Voter Pamphlet Distribution",
            'hi': "मानक मतदाता पुस्तिका वितरण बनाए रखें",
            'kn': "ಸಾಮಾನ್ಯ ಮತದಾರರ ಕರಪತ್ರ ವಿತರಣೆಯನ್ನು ಮುಂದುವರಿಸಿ"
        }
    }
    
    translated_reasons = {
        "Deficit mapped to general voter apathy metrics.": {
            'en': "Deficit mapped to general voter apathy metrics.",
            'hi': "घाटा सामान्य मतदाता उदासीनता मेट्रिक्स से संबंधित है।",
            'kn': "ಕೊರತೆಯು ಸಾಮಾನ್ಯ ಮತದಾರರ ಉದಾಸೀನತೆ ಮೆಟ್ರಿಕ್ಸ್‌ಗೆ ಸಂಬಂಧಿಸಿದೆ."
        },
        "Deficit mapped to low civic awareness metrics.": {
            'en': "Deficit mapped to low civic awareness metrics.",
            'hi': "घाटा कम नागरिक जागरूकता मेट्रिक्स से संबंधित है।",
            'kn': "ಕೊರತೆಯು ಕಡಿಮೆ ನಾಗರಿಕ ಜಾಗೃತಿ ಮೆಟ್ರಿಕ್ಸ್‌ಗೆ ಸಂಬಂಧಿಸಿದೆ."
        },
        "Deficit mapped to transportation access gaps metrics.": {
            'en': "Deficit mapped to transportation access gaps metrics.",
            'hi': "घाटा परिवहन पहुंच अंतराल मेट्रिक्स से संबंधित है।",
            'kn': "ಕೊರತೆಯು ಸಾರಿಗೆ ಪ್ರವೇಶದ ಕೊರತೆ ಮೆಟ್ರಿಕ್ಸ್‌ಗೆ ಸಂಬಂಧಿಸಿದೆ."
        },
        "Deficit mapped to severe weather drag metrics.": {
            'en': "Deficit mapped to severe weather drag metrics.",
            'hi': "घाटा गंभीर मौसम प्रभाव मेट्रिक्स से संबंधित है।",
            'kn': "ಕೊರತೆಯು ವಿಪರೀತ ಹವಾಮಾನ ಪ್ರಭಾವ ಮೆಟ್ರಿಕ್ಸ್‌ಗೆ ಸಂಬಂಧಿಸಿದೆ."
        },
        "Deficit mapped to low youth engagement metrics.": {
            'en': "Deficit mapped to low youth engagement metrics.",
            'hi': "घाटा कम युवा जुड़ाव मेट्रिक्स से संबंधित है।",
            'kn': "ಕೊರತೆಯು ಕಡಿಮೆ ಯುವ ಭಾಗವಹಿಸುವಿಕೆ ಮೆಟ್ರಿಕ್ಸ್‌ಗೆ ಸಂಬಂಧಿಸಿದೆ."
        },
        "Secondary reinforcement channel to boost participation.": {
            'en': "Secondary reinforcement channel to boost participation.",
            'hi': "भागीदारी बढ़ाने के लिए द्वितीयक सुदृढीकरण चैनल।",
            'kn': "ಭಾಗವಹಿಸುವಿಕೆಯನ್ನು ಹೆಚ್ಚಿಸಲು ದ್ವಿತೀಯ ಬಲವರ್ಧನೆ ಮಾರ್ಗ."
        },
        "Reinforce standard voting booths location mapping.": {
            'en': "Reinforce standard voting booths location mapping.",
            'hi': "मानक मतदान केंद्रों के स्थान मानचित्रण को सुदृढ़ करें।",
            'kn': "ಸಾಮಾನ್ಯ ಮತಗಟ್ಟೆಗಳ ಸ್ಥಳ ವಿವರಣೆಯನ್ನು ಬಲಪಡಿಸಿ."
        }
    }
    
    translated_difficulties = {
        "Easy": {'en': "Easy", 'hi': "आसान", 'kn': "ಸುಲಭ"},
        "Medium": {'en': "Medium", 'hi': "मध्यम", 'kn': "ಮಧ್ಯಮ"},
        "Hard": {'en': "Hard", 'hi': "कठिन", 'kn': "ಕಠಿಣ"}
    }

    cards = []
    for idx, r in enumerate(recommendations):
        rank = idx + 1
        risk_color = 'danger' if r['risk_level'] == 'High' else ('warning' if r['risk_level'] == 'Medium' else 'success')
        t_risk = t[r['risk_level'].lower()]
        
        action_boxes = []
        for action in r['actions']:
            t_act = translated_actions.get(action['action'], {}).get(lang, action['action'])
            t_reason = translated_reasons.get(action['reason'], {}).get(lang, action['reason'])
            t_difficulty = translated_difficulties.get(action['difficulty'], {}).get(lang, action['difficulty'])
            
            # Format impact nicely
            impact_text = action['impact']
            if 'Turnout' in impact_text:
                val = impact_text.split('%')[0]
                if lang == 'hi':
                    impact_text = f"{val}% मतदान वृद्धि"
                elif lang == 'kn':
                    impact_text = f"{val}% ಮತದಾನ ಹೆಚ್ಚಳ"

            action_boxes.append(
                dbc.Col([
                    html.Div([
                        html.Div(t_act, style={'fontWeight': '600', 'color': '#F8FAFC', 'fontSize': '0.9rem'}),
                        html.Div(t_reason, style={'fontSize': '0.75rem', 'color': '#94A3B8', 'marginTop': '0.2rem'}),
                        html.Div([
                            html.Span(f"{t['lbl_expected_gain']}: {impact_text}", className="badge bg-success text-white me-2", style={'fontSize': '0.7rem', 'backgroundColor': 'rgba(34, 197, 94, 0.15) !important'}),
                            html.Span(f"{t['lbl_difficulty']}: {t_difficulty}", className="badge bg-secondary", style={'fontSize': '0.7rem'})
                        ], className="d-flex mt-2")
                    ], className="border border-secondary rounded p-3 mb-2 h-100", style={'backgroundColor': '#0F1626'})
                ], md=6, xs=12)
            )
            
        t_issue = translated_problems.get(r['primary_issue'], {}).get(lang, r['primary_issue'])
            
        card = dbc.Card([
            dbc.Row([
                # Left Rank and Meta Col
                dbc.Col([
                    html.Div([
                        html.Div(f"#{rank}", style={'fontSize': '1.8rem', 'fontWeight': 'bold', 'color': '#60A5FA', 'fontFamily': 'Poppins'}),
                        html.Div(t['lbl_strategic_rank'], style={'fontSize': '0.65rem', 'color': '#94A3B8'})
                    ], className="text-center mb-2"),
                    
                    html.Div([
                        html.Span(f"{t['lbl_priority_index']}: {r['priority_score']:.1f}", className="badge bg-dark border border-secondary text-light", style={'fontSize': '0.75rem'})
                    ], className="text-center")
                ], xl=2, lg=2, md=3, xs=4, className="d-flex flex-column justify-content-center border-end border-secondary py-2"),
                
                # Middle Info Col
                dbc.Col([
                    html.H5(r['constituency'], style={'fontWeight': 'bold', 'color': '#F8FAFC', 'margin': 0}),
                    html.P(f"{r['district']} district, {r['state']}" if lang == 'en' else (f"{r['district']} जिला, {r['state']}" if lang == 'hi' else f"{r['district']} ಜಿಲ್ಲೆ, {r['state']}"), style={'color': '#94A3B8', 'fontSize': '0.8rem', 'marginBottom': '0.8rem'}),
                    
                    dbc.Row([
                        dbc.Col([
                            html.Div(t['lbl_early_turnout'], style={'fontSize': '0.7rem', 'color': '#94A3B8'}),
                            html.Div(f"{r['current_turnout']}%", style={'fontWeight': 'bold', 'fontSize': '1.0rem', 'color': '#F8FAFC'})
                        ], xs=4),
                        dbc.Col([
                            html.Div(t['lbl_historical_target'], style={'fontSize': '0.7rem', 'color': '#94A3B8'}),
                            html.Div(f"{r['historical_turnout']}%", style={'fontWeight': 'bold', 'fontSize': '1.0rem', 'color': '#F8FAFC'})
                        ], xs=4),
                        dbc.Col([
                            html.Div(t['lbl_risk_rating'], style={'fontSize': '0.7rem', 'color': '#94A3B8'}),
                            html.Span(t_risk, className=f"badge bg-{risk_color} mt-1", style={'fontSize': '0.75rem'})
                        ], xs=4)
                    ], className="g-0 mb-2"),
                    
                    # Diagnosed Issue line
                    html.Div([
                        html.Span(t['lbl_diagnosed_barrier'], style={'fontSize': '0.75rem', 'color': '#94A3B8'}),
                        html.Span(t_issue, style={'fontSize': '0.8rem', 'color': '#FACC15', 'fontWeight': '600'})
                    ], className="border-top border-secondary pt-2", style={'borderColor': 'rgba(30, 41, 59, 0.4)'})
                ], xl=4, lg=4, md=5, xs=8, className="ps-3 py-2"),
                
                # Right Actions Col
                dbc.Col([
                    html.Div(t['lbl_prescriptive_actions'], className="card-title-custom mb-2", style={'fontSize': '0.75rem'}),
                    dbc.Row(action_boxes, className="g-2")
                ], xl=6, lg=6, md=12, xs=12, className="py-2")
            ], className="g-0 align-items-center")
        ], className="stat-card mb-3", style={'padding': '1rem 1.5rem'})
        
        cards.append(card)
        
    return html.Div(cards)
