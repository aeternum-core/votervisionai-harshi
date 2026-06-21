from dash import html
import dash_bootstrap_components as dbc
import sys
import os

# Ensure parent directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import config

PAGE_TRANSLATIONS = {
    'en': {
        'title': "Methodology & Innovation Blueprint",
        'subtitle': "Project objectives, comparison matrix, algorithm audits, and official disclosure notices for VoteVision AI.",
        
        'innovation_header': "Innovation Statement",
        'innovation_p1': "Traditional dashboards mainly focus on ",
        'innovation_p2': "Descriptive Analytics",
        'innovation_p3': " (displaying historic and early turnout figures after they occur). ",
        'innovation_p4': "VoteVision AI",
        'innovation_p5': " transforms election analytics into ",
        'innovation_p6': "Predictive Intelligence",
        'innovation_p7': " (forecasting final turnout using Machine Learning) and ",
        'innovation_p8': "Prescriptive Intelligence",
        'innovation_p9': " (diagnosing regional barriers and recommending action recipes to administrative officers).",
        
        'creator_header': "Developer Profile",
        'creator_name': "Harshitha C",
        'creator_role': "Lead Architect & Developer",
        'creator_desc': "VoteVision AI is an advanced Election Decision Intelligence Platform designed to modernize election analytics through predictive and prescriptive intelligence. By combining machine learning, real-time data visualization, risk assessment models, and explainable AI, the platform enables election administrators to forecast voter turnout, identify participation risks, evaluate intervention strategies, and make data-driven decisions to improve civic engagement.",
        
        'badge_python': "Python / Dash",
        'badge_scikit': "Scikit-Learn ML",
        'badge_data_viz': "Data Visualization",
        
        'features_header': "Core Platform Features",
        
        'feat_pulse_lbl': "National Election Pulse™: ",
        'feat_pulse_val': "A live aggregate turnout health indicator (Pulse Score out of 100) combining forecasted risk scores and averages.",
        
        'feat_forecast_lbl': "AI Turnout Forecasts: ",
        'feat_forecast_val': "Uses Random Forest Regressors to forecast final turnout and interactive Plotly speedometers to show prediction confidence.",
        
        'feat_xai_lbl': "Explainable AI (XAI) Panel: ",
        'feat_xai_val': "Calculates local feature contribution drivers (transport accessibility, campaign boosts, holidays, weather) for trust validation.",
        
        'feat_sim_lbl': "What-If Simulator Sandbox: ",
        'feat_sim_val': "Test adjustments to campaign intensity, transport, or weather comfort, with quick-apply presets (Torrential Rain, Holiday Drag).",
        
        'feat_advisor_lbl': "Election Strategy Advisor™: ",
        'feat_advisor_val': "Diagnoses local civic barriers and ranks constituencies in a prioritized strategy recommendation log.",
        
        'feat_risk_lbl': "AI Risk Intelligence: ",
        'feat_risk_val': "Flags underperforming zones based on historical baseline deviations and registers them in a central operations log.",
        
        'formulas_header': "System Formula Audits",
        
        'formula_pulse_lbl': "1. National Election Pulse™",
        'formula_pulse_desc': "Overall participation velocity indicator based on turnout, EHS index, and risk values:",
        
        'formula_ehs_lbl': "2. Election Health Score (EHS)™",
        'formula_ehs_desc': "Calculated programmatically to determine regional administrative stability index:",
        'formula_ehs_note1': "MomentumFactor: Accelerating=100 | Stable=75 | Declining=50",
        'formula_ehs_note2': "RiskPenalty: High=100 | Medium=50 | Low=0",
        
        'formula_cis_lbl': "3. Civic Impact Score™",
        'formula_cis_desc': "Proprietary indicator combining infrastructure access and localized campaigning parameters:",
        
        'formula_ypi_lbl': "4. Youth Participation Index™",
        'formula_ypi_desc': "Modeled to reflect youth demographics engagement relative to awareness outreach metrics:",
        
        'ml_header': "Machine Learning Pipelines",
        
        'ml_xai_lbl': "Explainable AI (XAI) feature importance drivers",
        'ml_xai_desc': "Each prediction isolates demographic, transport access, holiday drag, and weather comfort features. It calculates exact positive/negative contributions to show why the AI model predicted specific final turnout percentages.",
        
        'ml_rf_lbl': "Random Forest Algorithms",
        'ml_rf_desc': "Regression models forecast turnout percentages while Classification models categorize risk levels into Low, Medium, and High risk classifications.",
        
        'tech_header': "Technical Stack Modules",
        'tech_item_1': "Python 3.13.9: Core program architecture & pandas ETL pipelines.",
        'tech_item_2': "Dash & Bootstrap Components: Interactive UI layouts and HTML wrappers.",
        'tech_item_3': "Plotly: Dynamic responsive chart drawing engines.",
        'tech_item_4': "Scikit-Learn & Joblib: ML model fitting, evaluation, and serialization.",
        
        'disclaimer_title': "Academic Civic-Tech Disclaimer",
        'disclaimer_desc': "This dashboard represents an academic simulation application. It does not represent, predict, or casting official election results for the Election Commission of India. All metrics, calculations, model outcomes, and geographic structures are generated synthetically for academic demonstration, auditing, and analytics evaluation purposes.",
        
        'tbl_header_matrix': "System Comparison Matrix",
        'tbl_header_matrix_desc': "How VoteVision AI compares to standard descriptive dashboards used in election reports:",
        'tbl_th_audit': "Feature Audit",
        'tbl_th_existing': "Existing Election Systems",
        'tbl_th_proposed': "VoteVision AI (Proposed)",
        
        'tbl_td_turnout': "Turnout Analytics",
        'tbl_td_turnout_exist': "Descriptive: Reports past turnout percentages only.",
        'tbl_td_turnout_prop': "Predictive & Prescriptive: Forecasts live progressive outcomes and recommends turnout recovery plans.",
        
        'tbl_td_decision': "Decision Support",
        'tbl_td_decision_exist': "None: Static dashboard reports metrics.",
        'tbl_td_decision_prop': "Prescriptive: Mapped administrative strategies based on socio-economic barriers.",
        
        'tbl_td_sim': "Operational Simulator",
        'tbl_td_sim_exist': "None: No scenario evaluation possible.",
        'tbl_td_sim_prop': "Simulation: Live What-If Sandbox to test effects of campaigns, transport shuttles, and weather adjustments.",
        
        'tbl_td_risk': "Risk Detection",
        'tbl_td_risk_exist': "Manual: Analysts must visually isolate drops.",
        'tbl_td_risk_prop': "AI Risk Detector: Automatic anomaly alert indexing for early warnings.",
        
        'tbl_td_relevance': "India Specific Relevance",
        'tbl_td_relevance_exist': "Generic: Overall global demographic views.",
        'tbl_td_relevance_prop': "Targeted: State/District drilldown, multilingual presets, and Youth Participation Index™."
    },
    'hi': {
        'title': "पद्धति और नवाचार खाका",
        'subtitle': "मतदृष्टि एआई के लिए परियोजना उद्देश्य, तुलनात्मक मैट्रिक्स, एल्गोरिदम ऑडिट और आधिकारिक प्रकटीकरण नोटिस।",
        
        'innovation_header': "नवाचार वक्तव्य (Statement)",
        'innovation_p1': "पारंपरिक डैशबोर्ड मुख्य रूप से ",
        'innovation_p2': "वर्णनात्मक विश्लेषण (Descriptive Analytics)",
        'innovation_p3': " (ऐतिहासिक और प्रारंभिक मतदान के आंकड़े प्रदर्शित करने) पर ध्यान केंद्रित करते हैं। ",
        'innovation_p4': "मतदृष्टि एआई",
        'innovation_p5': " चुनाव विश्लेषण को ",
        'innovation_p6': "पूर्वानुमानित बुद्धिमत्ता (Predictive Intelligence)",
        'innovation_p7': " (मशीन लर्निंग का उपयोग करके अंतिम मतदान का पूर्वानुमान लगाना) और ",
        'innovation_p8': "प्रिस्क्रिप्टिव इंटेलिजेंस (Prescriptive Intelligence)",
        'innovation_p9': " (क्षेत्रीय बाधाओं का निदान करना और प्रशासनिक अधिकारियों को कार्रवाई के नुस्खे सुझाना) में बदल देता है।",
        
        'creator_header': "डेवलपर प्रोफाइल",
        'creator_name': "हर्षिता सी",
        'creator_role': "मुख्य वास्तुकार और डेवलपर",
        'creator_desc': "मतदृष्टि एआई (VoteVision AI) एक उन्नत चुनाव निर्णय खुफिया मंच है जिसे भविष्य कहनेवाला और वर्णनात्मक खुफिया के माध्यम से चुनाव विश्लेषण को आधुनिक बनाने के लिए डिज़ाइन किया गया है। मशीन लर्निंग, वास्तविक समय डेटा विज़ुअलाइज़ेशन, जोखिम मूल्यांकन मॉडल और व्याख्यात्मक एआई को मिलाकर, यह मंच चुनाव प्रशासकों को मतदाता मतदान का पूर्वानुमान लगाने, भागीदारी जोखिमों की पहचान करने, हस्तक्षेप रणनीतियों का मूल्यांकन करने और नागरिक जुड़ाव को बेहतर बनाने के लिए डेटा-संचालित निर्णय लेने में सक्षम बनाता है।",
        
        'badge_python': "पायथन / डैश",
        'badge_scikit': "साइकिट-लर्न एमएल",
        'badge_data_viz': "डेटा विज़ुअलाइज़ेशन",
        
        'features_header': "मंच की मुख्य विशेषताएं",
        
        'feat_pulse_lbl': "राष्ट्रीय चुनाव पल्स™: ",
        'feat_pulse_val': "एक लाइव समग्र मतदान स्वास्थ्य सूचक (100 में से पल्स स्कोर) जो अनुमानित जोखिम स्कोर और औसत को जोड़ता है।",
        
        'feat_forecast_lbl': "एआई मतदान पूर्वानुमान: ",
        'feat_forecast_val': "अंतिम मतदान का पूर्वानुमान लगाने के लिए रैंडम फॉरेस्ट रिग्रेसर्स और पूर्वानुमान आत्मविश्वास दिखाने के लिए इंटरैक्टिव Plotly स्पीडोमीटर का उपयोग करता है।",
        
        'feat_xai_lbl': "व्याख्यात्मक एआई (XAI) पैनल: ",
        'feat_xai_val': "विश्वास सत्यापन के लिए स्थानीय कारक योगदान चालकों (परिवहन सुलभता, अभियान प्रचार, छुट्टियां, मौसम) की गणना करता है।",
        
        'feat_sim_lbl': "व्हाट-इफ सिमुलेटर सैंडबॉक्स: ",
        'feat_sim_val': "त्वरित-लागू प्रीसेट (मूसलाधार बारिश, छुट्टी का प्रभाव) के साथ अभियान की तीव्रता, परिवहन, या मौसम के आराम में समायोजन का परीक्षण करें।",
        
        'feat_advisor_lbl': "चुनाव रणनीति सलाहकार™: ",
        'feat_advisor_val': "स्थानीय नागरिक बाधाओं का निदान करता है और प्राथमिकता वाले रणनीति अनुशंसा लॉग में निर्वाचन क्षेत्रों को रैंक करता है।",
        
        'feat_risk_lbl': "एआई जोखिम इंटेलिजेंस: ",
        'feat_risk_val': "ऐतिहासिक आधारभूत विचलन के आधार पर खराब प्रदर्शन करने वाले क्षेत्रों को चिह्नित करता है और उन्हें केंद्रीय संचालन लॉग में दर्ज करता है।",
        
        'formulas_header': "प्रणाली सूत्र ऑडिट",
        
        'formula_pulse_lbl': "1. राष्ट्रीय चुनाव पल्स™",
        'formula_pulse_desc': "मतदान, ईएचएस सूचकांक और जोखिम मूल्यों पर आधारित समग्र भागीदारी वेग सूचक:",
        
        'formula_ehs_lbl': "2. चुनाव स्वास्थ्य स्कोर (EHS)™",
        'formula_ehs_desc': "क्षेत्रीय प्रशासनिक स्थिरता सूचकांक निर्धारित करने के लिए प्रोग्रामेटिक रूप से गणना की गई:",
        'formula_ehs_note1': "गति कारक (MomentumFactor): तेजी से बढ़ता हुआ=100 | स्थिर=75 | घटता हुआ=50",
        'formula_ehs_note2': "जोखिम दंड (RiskPenalty): उच्च=100 | मध्यम=50 | कम=0",
        
        'formula_cis_lbl': "3. नागरिक प्रभाव स्कोर™",
        'formula_cis_desc': "बुनियादी ढांचा पहुंच और स्थानीयकृत प्रचार मापदंडों को मिलाने वाला संकेतक:",
        
        'formula_ypi_lbl': "4. युवा भागीदारी सूचकांक™",
        'formula_ypi_desc': "जागरूकता आउटरीच मेट्रिक्स के सापेक्ष युवा जनसांख्यिकी जुड़ाव को प्रतिबिंबित करने के लिए तैयार किया गया:",
        
        'ml_header': "मशीन लर्निंग पाइपलाइन्स",
        
        'ml_xai_lbl': "व्याख्यात्मक एआई (XAI) विशेषता महत्व चालक",
        'ml_xai_desc': "प्रत्येक पूर्वानुमान जनसांख्यिकीय, परिवहन पहुंच, छुट्टी के प्रभाव और मौसम के आराम की विशेषताओं को अलग करता है। यह सटीक सकारात्मक/नकारात्मक योगदान की गणना करता है जिससे पता करता है कि एआई मॉडल ने विशिष्ट अंतिम मतदान प्रतिशत की भविष्यवाणी क्यों की।",
        
        'ml_rf_lbl': "रैंडम फॉरेस्ट एल्गोरिदम",
        'ml_rf_desc': "रिग्रेशन मॉडल मतदान प्रतिशत का पूर्वानुमान लगाते हैं जबकि वर्गीकरण मॉडल जोखिम के स्तरों को निम्न, मध्यम और उच्च जोखिम श्रेणियों में वर्गीकृत करते हैं।",
        
        'tech_header': "तकनीकी स्टैक मॉड्यूल",
        'tech_item_1': "पायथन 3.13.9: कोर प्रोग्राम आर्किटेक्चर और पांडा ईटीएल पाइपलाइन।",
        'tech_item_2': "डैश और बूटस्ट्रैप घटक: इंटरैक्टिव यूआई लेआउट और HTML रैपर।",
        'tech_item_3': "Plotly: डायनामिक उत्तरदायी चार्ट ड्राइंग इंजन।",
        'tech_item_4': "साइकिट-लर्न और जॉबलिब: एमएल मॉडल फिटिंग, मूल्यांकन और सीरियलाइजेशन।",
        
        'disclaimer_title': "अकादमिक सिविक-टेक अस्वीकरण",
        'disclaimer_desc': "यह डैशबोर्ड एक अकादमिक सिमुलेशन अनुप्रयोग का प्रतिनिधित्व करता है। यह भारत निर्वाचन आयोग के आधिकारिक चुनाव परिणामों का प्रतिनिधित्व, पूर्वानुमान या प्रसारण नहीं करता है। सभी मेट्रिक्स, गणना, मॉडल परिणाम और भौगोलिक संरचनाएं अकादमिक प्रदर्शन, ऑडिटिंग और विश्लेषण मूल्यांकन उद्देश्यों के लिए कृत्रिम रूप से उत्पन्न की गई हैं।",
        
        'tbl_header_matrix': "प्रणाली तुलना मैट्रिक्स",
        'tbl_header_matrix_desc': "चुनाव रिपोर्टों में उपयोग किए जाने वाले मानक वर्णनात्मक डैशबोर्ड की तुलना में मतदृष्टि एआई कैसा प्रदर्शन करता है:",
        'tbl_th_audit': "विशेषता ऑडिट",
        'tbl_th_existing': "मौजूदा चुनाव प्रणालियां",
        'tbl_th_proposed': "मतदृष्टि एआई (प्रस्तावित)",
        
        'tbl_td_turnout': "मतदान विश्लेषण",
        'tbl_td_turnout_exist': "वर्णनात्मक: केवल पिछले मतदान प्रतिशत की रिपोर्ट करता है।",
        'tbl_td_turnout_prop': "पूर्वानुमानित और निर्देशात्मक: लाइव प्रगतिशील परिणामों का पूर्वानुमान लगाता है और मतदान वसूली योजनाओं की सिफारिश करता है।",
        
        'tbl_td_decision': "निर्णय समर्थन",
        'tbl_td_decision_exist': "कोई नहीं: स्थिर डैशबोर्ड केवल मेट्रिक्स की रिपोर्ट करता है।",
        'tbl_td_decision_prop': "निर्देशात्मक: सामाजिक-आर्थिक बाधाओं के आधार पर प्रशासनिक रणनीतियों का मानचित्रण।",
        
        'tbl_td_sim': "परिचालन सिम्युलेटर",
        'tbl_td_sim_exist': "कोई नहीं: कोई परिदृश्य मूल्यांकन संभव नहीं है।",
        'tbl_td_sim_prop': "सिमुलेशन: अभियानों, परिवहन शटल और मौसम समायोजन के प्रभावों का परीक्षण करने के लिए लाइव व्हाट-इफ सैंडबॉक्स।",
        
        'tbl_td_risk': "जोखिम का पता लगाना",
        'tbl_td_risk_exist': "मैनुअल: विश्लेषकों को दृश्य रूप से कमियों को अलग करना होगा।",
        'tbl_td_risk_prop': "एआई जोखिम डिटेक्टर: प्रारंभिक चेतावनी के लिए स्वचालित विसंगति चेतावनी अनुक्रमण।",
        
        'tbl_td_relevance': "भारत विशिष्ट प्रासंगिकता",
        'tbl_td_relevance_exist': "सामान्य: समग्र वैश्विक जनसांख्यिकीय दृश्य।",
        'tbl_td_relevance_prop': "लक्षित: राज्य/जिला ड्रिलडाउन, बहुभाषी प्रीसेट, और युवा भागीदारी सूचकांक™।"
    },
    'kn': {
        'title': "ವಿಧಾನ ಮತ್ತು ನಾವೀನ್ಯತೆಯ ನೀಲನಕ್ಷೆ",
        'subtitle': "ಮತವಿಷನ್ ಎಐ ಗಾಗಿ ಯೋಜನೆಯ ಉದ್ದೇಶಗಳು, ಹೋಲಿಕೆ ಮ್ಯಾಟ್ರಿಕ್ಸ್, ಅಲ್ಗಾರಿದಮ್ ಆಡಿಟ್‌ಗಳು ಮತ್ತು ಅಧಿಕೃತ ಪ್ರಕಟಣೆಗಳು.",
        
        'innovation_header': "ನಾವೀನ್ಯತೆಯ ಹೇಳಿಕೆ",
        'innovation_p1': "ಸಾಂಪ್ರದಾಯಿಕ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ಗಳು ಮುಖ್ಯವಾಗಿ ",
        'innovation_p2': "ವರ್ಣನಾತ್ಮಕ ವಿಶ್ಲೇಷಣೆ (Descriptive Analytics)",
        'innovation_p3': " (ಹಿಂದಿನ ಮತ್ತು ಆರಂಭಿಕ ಮತದಾನದ ಪ್ರಮಾಣವನ್ನು ಅವು ಸಂಭವಿಸಿದ ನಂತರ ಪ್ರದರ್ಶಿಸುವುದು) ಮೇಲೆ ಗಮನ ಹರಿಸುತ್ತವೆ. ",
        'innovation_p4': "ಮತವಿಷನ್ ಎಐ",
        'innovation_p5': " ಚುನಾವಣಾ ವಿಶ್ಲೇಷಣೆಯನ್ನು ",
        'innovation_p6': "ಮುನ್ಸೂಚಕ ಬುದ್ಧಿಮತ್ತೆ (Predictive Intelligence)",
        'innovation_p7': " (ಮಷಿನ್ ಲರ್ನಿಂಗ್ ಬಳಸಿ ಅಂತಿಮ ಮತದಾನವನ್ನು ಮುನ್ಸೂಚಿಸುವುದು) ಮತ್ತು ",
        'innovation_p8': "ಪ್ರಿಸ್ಕ್ರಿಪ್ಟಿವ್ ಇಂಟೆಲಿಜೆನ್ಸ್ (Prescriptive Intelligence)",
        'innovation_p9': " (ಪ್ರಾದೇಶಿಕ ಅಡಚಣೆಗಳನ್ನು ಪತ್ತೆಹಚ್ಚುವುದು ಮತ್ತು ಆಡಳಿತಾಧಿಕಾರಿಗಳಿಗೆ ಪರಿಹಾರ ಕ್ರಮಗಳನ್ನು ಶಿಫಾರಸು ಮಾಡುವುದು) ಆಗಿ ಪರಿವರ್ತಿಸುತ್ತದೆ.",
        
        'creator_header': "ಡೆವಲಪರ್ ಪ್ರೊಫೈಲ್",
        'creator_name': "ಹರ್ಷಿತಾ ಸಿ",
        'creator_role': "ಮುಖ್ಯ ಆರ್ಕಿಟೆಕ್ಟ್ ಮತ್ತು ಡೆವಲಪರ್",
        'creator_desc': "ಮತವಿಷನ್ ಎಐ (VoteVision AI) ಎನ್ನುವುದು ಮುನ್ಸೂಚಕ ಮತ್ತು ಪ್ರಿಸ್ಕ್ರಿಪ್ಟಿವ್ ಬುದ್ಧಿಮತ್ತೆಯ ಮೂಲಕ ಚುನಾವಣಾ ವಿಶ್ಲೇಷಣೆಯನ್ನು ಆಧುನೀಕರಿಸಲು ವಿನ್ಯಾಸಗೊಳಿಸಲಾದ ಸುಧಾರಿತ ಚುನಾವಣಾ ನಿರ್ಧಾರ ಗುಪ್ತಚರ ವೇದಿಕೆಯಾಗಿದೆ. ಮಷಿನ್ ಲರ್ನಿಂಗ್, ನೈಜ-ಸಮಯದ ಡೇಟಾ ದೃಶ್ಯೀಕರಣ, ಅಪಾಯ ಮೌಲ್ಯಮಾಪನ ಮಾದರಿಗಳು ಮತ್ತು ವಿವರಣಾತ್ಮಕ ಎಐ ಅನ್ನು ಸಂಯೋಜಿಸುವ ಮೂಲಕ, ವೇದಿಕೆಯು ಚುನಾವಣಾ ಆಡಳಿತಾಧಿಕಾರಿಗಳಿಗೆ ಮತದಾರರ ಮತದಾನವನ್ನು ಮುನ್ಸೂಚಿಸಲು, ಭಾಗವಹಿಸುವಿಕೆಯ ಅಪಾಯಗಳನ್ನು ಗುರುತಿಸಲು, ಹಸ್ತಕ್ಷೇಪದ ಕಾರ್ಯತಂತ್ರಗಳನ್ನು ಮೌಲ್ಯಮಾಪನ ಮಾಡಲು ಮತ್ತು ನಾಗರಿಕ ತೊಡಗಿಸಿಕೊಳ್ಳುವಿಕೆಯನ್ನು ಸುಧಾರಿಸಲು ಡೇಟಾ-ಚಾಲಿತ ನಿರ್ಧಾರಗಳನ್ನು ತೆಗೆದುಕೊಳ್ಳಲು ಅನುವು ಮಾಡಿಕೊಡುತ್ತದೆ.",
        
        'badge_python': "ಪೈಥಾನ್ / ಡ್ಯಾಶ್",
        'badge_scikit': "ಸೈಕಿಟ್-ಲರ್ನ್ ಎಮ್ಎಲ್",
        'badge_data_viz': "ಡೇಟಾ ದೃಶ್ಯೀಕರಣ",
        
        'features_header': "ವೇದಿಕೆಯ ಪ್ರಮುಖ ವೈಶಿಷ್ಟ್ಯಗಳು",
        
        'feat_pulse_lbl': "ರಾಷ್ಟ್ರೀಯ ಚುನಾವಣಾ ಪಲ್ಸ್™: ",
        'feat_pulse_val': "ಮುನ್ಸೂಚಿತ ಅಪಾಯದ ಸ್ಕೋರ್‌ಗಳು ಮತ್ತು ಸರಾಸರಿಗಳನ್ನು ಸಂಯೋಜಿಸುವ ಲೈವ್ ಒಟ್ಟಾರೆ ಮತದಾನ ಆರೋಗ್ಯ ಸೂಚಕ (100 ರಲ್ಲಿ ಪಲ್ಸ್ ಸ್ಕೋರ್).",
        
        'feat_forecast_lbl': "ಎಐ ಮತದಾನ ಮುನ್ಸೂಚನೆಗಳು: ",
        'feat_forecast_val': "ಅಂತಿಮ ಮತದಾನವನ್ನು ಮುನ್ಸೂಚಿಸಲು ರಾಂಡಮ್ ಫಾರೆಸ್ಟ್ ರಿಗ್ರೆಸರ್‌ಗಳನ್ನು ಮತ್ತು ಮುನ್ಸೂಚನೆಯ ವಿಶ್ವಾಸಾರ್ಹತೆಯನ್ನು ತೋರಿಸಲು ಸಂವಾದಾತ್ಮಕ Plotly ಸ್ಪೀಡೋಮೀಟರ್ ಅನ್ನು ಬಳಸುತ್ತದೆ.",
        
        'feat_xai_lbl': "ವಿವರಣಾತ್ಮಕ ಎಐ (XAI) ಫಲಕ: ",
        'feat_xai_val': "ವಿಶ್ವಾಸಾರ್ಹತೆ ಪರಿಶೀಲನೆಗಾಗಿ ಸ್ಥಳೀಯ ವೈಶಿಷ್ಟ್ಯ ಕೊಡುಗೆ ಚಾಲಕಗಳನ್ನು (ಸಾರಿಗೆ ಪ್ರವೇಶ, ಪ್ರಚಾರದ ಹೆಚ್ಚಳ, ರಜಾದಿನಗಳು, ಹವಾಮಾನ) ಲೆಕ್ಕಾಚಾರ ಮಾಡುತ್ತದೆ.",
        
        'feat_sim_lbl': "ವಾಟ್-ಇಫ್ ಸಿಮ್ಯುಲೇಟರ್ ಸ್ಯಾಂಡ್‌ಬಾಕ್ಸ್: ",
        'feat_sim_val': "ತ್ವರಿತವಾಗಿ ಅನ್ವಯಿಸಬಹುದಾದ ಪ್ರಿಸೆಟ್‌ಗಳೊಂದಿಗೆ (ವಿಪರೀತ ಮಳೆ, ರಜಾದಿನದ ಡ್ರ್ಯಾಗ್) ಪ್ರಚಾರದ ತೀವ್ರತೆ, ಸಾರಿಗೆ ಅಥವಾ ಹವಾಮಾನ ಕಂಫರ್ಟ್‌ಗೆ ಹೊಂದಾಣಿಕೆಗಳನ್ನು ಪರೀಕ್ಷಿಸಿ.",
        
        'feat_advisor_lbl': "ಚುನಾವಣಾ ಕಾರ್ಯತಂತ್ರ ಸಲಹೆಗಾರ™: ",
        'feat_advisor_val': "ಸ್ಥಳೀಯ ನಾಗರಿಕ ಅಡೆತಡೆಗಳನ್ನು ಪತ್ತೆಹಚ್ಚುತ್ತದೆ ಮತ್ತು ಆದ್ಯತೆಯ ಕಾರ್ಯತಂತ್ರದ ಶಿಫಾರಸು ಲಾಗ್‌ನಲ್ಲಿ ಮತಕ್ಷೇತ್ರಗಳನ್ನು ಶ್ರೇಣೀಕರಿಸುತ್ತದೆ.",
        
        'feat_risk_lbl': "ಎಐ ಅಪಾಯ ವಿಶ್ಲೇಷಣೆ: ",
        'feat_risk_val': "ಐತಿಹಾಸಿಕ ಬೇಸ್‌ಲೈನ್ ವಿಚಲನಗಳ ಆಧಾರದ ಮೇಲೆ ಕಡಿಮೆ ಮತದಾನದ ಪ್ರದೇಶಗಳನ್ನು ಗುರುತಿಸುತ್ತದೆ ಮತ್ತು ಅವುಗಳನ್ನು ಕೇಂದ್ರ ಕಾರ್ಯಾಚರಣೆಗಳ ಲಾಗ್‌ನಲ್ಲಿ ದಾಖಲಿಸುತ್ತದೆ.",
        
        'formulas_header': "ವ್ಯವಸ್ಥೆಯ ಸೂತ್ರಗಳ ಆಡಿಟ್‌ಗಳು",
        
        'formula_pulse_lbl': "1. ರಾಷ್ಟ್ರೀಯ ಚುನಾವಣಾ ಪಲ್ಸ್™",
        'formula_pulse_desc': "ಮತದಾನ, ಇಹೆಚ್ಎಸ್ ಸೂಚ್ಯಂಕ ಮತ್ತು ಅಪಾಯದ ಮೌಲ್ಯಗಳ ಆಧಾರದ ಮೇಲೆ ಒಟ್ಟಾರೆ ಭಾಗವಹಿಸುವಿಕೆಯ ವೇಗದ ಸೂಚಕ:",
        
        'formula_ehs_lbl': "2. ಚುನಾವಣಾ ಆರೋಗ್ಯ ಸ್ಕೋರ್ (EHS)™",
        'formula_ehs_desc': "ಪ್ರಾದೇಶಿಕ ಆಡಳಿತಾತ್ಮಕ ಸ್ಥಿರತೆಯ ಸೂಚ್ಯಂಕವನ್ನು ನಿರ್ಧರಿಸಲು ಪ್ರೋಗ್ರಾಮ್ಯಾಟಿಕ್ ಆಗಿ ಲೆಕ್ಕಹಾಕಲಾಗುತ್ತದೆ:",
        'formula_ehs_note1': "ವೇಗದ ಅಂಶ (MomentumFactor): ವೇಗವರ್ಧನೆ=100 | ಸ್ಥಿರ=75 | ಕುಸಿತ=50",
        'formula_ehs_note2': "ಅಪಾಯದ ದಂಡ (RiskPenalty): ಹೆಚ್ಚು=100 | ಮಧ್ಯಮ=50 | ಕಡಿಮೆ=0",
        
        'formula_cis_lbl': "3. ನಾಗರಿಕ ಪ್ರಭಾವದ ಸ್ಕೋರ್™",
        'formula_cis_desc': "ಮೂಲಸೌಕರ್ಯ ಪ್ರವೇಶ ಮತ್ತು ಸ್ಥಳೀಯ ಪ್ರಚಾರ ನಿಯತಾಂಕಗಳನ್ನು ಸಂಯೋಜಿಸುವ ಸ್ವಾಮ್ಯದ ಸೂಚಕ:",
        
        'formula_ypi_lbl': "4. ಯುವ ಭಾಗವಹಿಸುವಿಕೆ ಸೂಚ್ಯಂಕ™",
        'formula_ypi_desc': "ಜಾಗೃತಿ ಪ್ರಚಾರದ ಮೆಟ್ರಿಕ್‌ಗಳಿಗೆ ಹೋಲಿಸಿದರೆ ಯುವ ಮತದಾರರ ತೊಡಗಿಸಿಕೊಳ್ಳುವಿಕೆಯನ್ನು ಪ್ರತಿಬಿಂಬಿಸಲು ವಿನ್ಯಾಸಗೊಳಿಸಲಾಗಿದೆ:",
        
        'ml_header': "ಮಷಿನ್ ಲರ್ನಿಂಗ್ ಪೈಪ್‌ಲೈನ್‌ಗಳು",
        
        'ml_xai_lbl': "ವಿವರಣಾತ್ಮಕ ಎಐ (XAI) ವೈಶಿಷ್ಟ್ಯಗಳ ಪ್ರಾಮುಖ್ಯತೆಯ ಚಾಲಕರು",
        'ml_xai_desc': "ಪ್ರತಿ ಮುನ್ಸೂಚನೆಯು ಜನಸಂಖ್ಯಾ, ಸಾರಿಗೆ ಪ್ರವೇಶ, ರಜಾದಿನದ ಡ್ರ್ಯಾಗ್ ಮತ್ತು ಹವಾಮಾನ ಕಂಫರ್ಟ್ ವೈಶಿಷ್ಟ್ಯಗಳನ್ನು ಪ್ರತ್ಯೇಕಿಸುತ್ತದೆ. ಎಐ ಮಾದರಿಯು ನಿರ್ದಿಷ್ಟ ಅಂತಿಮ ಮತದಾನದ ಶೇಕಡಾವಾರು ಪ್ರಮಾಣವನ್ನು ಏಕೆ ಮುನ್ಸೂಚಿಸಿದೆ ಎಂಬುದನ್ನು ತೋರಿಸಲು ಇದು ನಿಖರವಾದ ಧನಾತ್ಮಕ/ಋಣಾತ್ಮಕ ಕೊಡುಗೆಗಳನ್ನು ಲೆಕ್ಕಾಚಾರ ಮಾಡುತ್ತದೆ.",
        
        'ml_rf_lbl': "ರಾಂಡಮ್ ಫಾರೆಸ್ಟ್ ಅಲ್ಗಾರಿದಮ್‌ಗಳು",
        'ml_rf_desc': "ರಿಗ್ರೆಶನ್ ಮಾದರಿಗಳು ಮತದಾನದ ಪ್ರಮಾಣವನ್ನು ಮುನ್ಸೂಚಿಸುತ್ತವೆ ಮತ್ತು ಕ್ಲಾಸಿಫಿಕೇಶನ್ ಮಾದರಿಗಳು ಅಪಾಯದ ಮಟ್ಟವನ್ನು ಕಡಿಮೆ, ಮಧ್ಯಮ ಮತ್ತು ಹೆಚ್ಚಿನ ಅಪಾಯದ ವರ್ಗಗಳಾಗಿ ವಿಂಗಡಿಸುತ್ತವೆ.",
        
        'tech_header': "ತಾಂತ್ರಿಕ ಸ್ಟ್ಯಾಕ್ ಮಾಡ್ಯೂಲ್‌ಗಳು",
        'tech_item_1': "ಪೈಥಾನ್ 3.13.9: ಕೋರ್ ಪ್ರೋಗ್ರಾಂ ಆರ್ಕಿಟೆಕ್ಚರ್ ಮತ್ತು ಪಾಂಡಾಸ್ ಇಟಿಎಲ್ ಪೈಪ್‌ಲೈನ್‌ಗಳು.",
        'tech_item_2': "ಡ್ಯಾಶ್ ಮತ್ತು ಬೂಟ್‌ಸ್ಟ್ರ್ಯಾಪ್ ಘಟಕಗಳು: ಸಂವಾದಾತ್ಮಕ ಯುಐ ಲೇಔಟ್‌ಗಳು ಮತ್ತು ಎಚ್‌ಟಿಎಮ್‌ಎಲ್ ರಾಪರ್‌ಗಳು.",
        'tech_item_3': "Plotly: ಡೈನಾಮಿಕ್ ರೆಸ್ಪಾನ್ಸಿವ್ ಚಾರ್ಟ್ ಡ್ರಾಯಿಂಗ್ ಎಂಜಿನ್ಗಳು.",
        'tech_item_4': "ಸೈಕಿಟ್-ಲರ್ನ್ ಮತ್ತು ಜಾಬ್ಲಿಬ್: ಎಮ್ಎಲ್ ಮಾಡೆಲ್ ಫಿಟ್ಟಿಂಗ್, ಮೌಲ್ಯಮಾಪನ ಮತ್ತು ಸೀರಿಯಲೈಸೇಶನ್.",
        
        'disclaimer_title': "ಶೈಕ್ಷಣಿಕ ಸಿವಿಕ್-ಟೆಕ್ ಹಕ್ಕುತ್ಯಾಗ",
        'disclaimer_desc': "ಈ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್ ಕೇವಲ ಶೈಕ್ಷಣಿಕ ಸಿಮ್ಯುಲೇಶನ್ ಅಪ್ಲಿಕೇಶನ್ ಆಗಿದೆ. ಇದು ಭಾರತೀಯ ಚುನಾವಣಾ ಆಯೋಗದ ಅಧಿಕೃತ ಚುನಾವಣಾ ಫಲಿತಾಂಶಗಳನ್ನು ಪ್ರತಿನಿಧಿಸುವುದಿಲ್ಲ, ಮುನ್ಸೂಚಿಸುವುದಿಲ್ಲ ಅಥವಾ ಪ್ರಕಟಿಸುವುದಿಲ್ಲ. ಎಲ್ಲಾ ಮೆಟ್ರಿಕ್‌ಗಳು, ಲೆಕ್ಕಾಚಾರಗಳು, ಮಾದರಿಯ ಫಲಿತಾಂಶಗಳು ಮತ್ತು ಭೌಗೋಳಿಕ ರಚನೆಗಳನ್ನು ಶೈಕ್ಷಣಿಕ ಪ್ರದರ್ಶನ, ಆಡಿಟಿಂಗ್ ಮತ್ತು ವಿಶ್ಲೇಷಣೆ ಮೌಲ್ಯಮಾಪನ ಉದ್ದೇಶಗಳಿಗಾಗಿ ಕೃತಕವಾಗಿ ರಚಿಸಲಾಗಿದೆ.",
        
        'tbl_header_matrix': "ಸಿಸ್ಟಮ್ ಹೋಲಿಕೆ ಮ್ಯಾಟ್ರಿಕ್ಸ್",
        'tbl_header_matrix_desc': "ಚುನಾವಣಾ ವರದಿಗಳಲ್ಲಿ ಬಳಸಲಾಗುವ ಸಾಮಾನ್ಯ ವರ್ಣನಾತ್ಮಕ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ಗಳಿಗೆ ಹೋಲಿಸಿದರೆ ಮತವಿಷನ್ ಎಐ ಹೇಗೆ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತದೆ:",
        'tbl_th_audit': "ವೈಶಿಷ್ಟ್ಯಗಳ ಆಡಿಟ್",
        'tbl_th_existing': "ಅಸ್ತಿತ್ವದಲ್ಲಿರುವ ಚುನಾವಣಾ ವ್ಯವಸ್ಥೆಗಳು",
        'tbl_th_proposed': "ಮತವಿಷನ್ ಎಐ (ಪ್ರಸ್ತಾವಿತ)",
        
        'tbl_td_turnout': "ಮತದಾನದ ವಿಶ್ಲೇಷಣೆ",
        'tbl_td_turnout_exist': "ವರ್ಣನಾತ್ಮಕ: ಹಿಂದಿನ ಮತದಾನದ ಪ್ರಮಾಣವನ್ನು ಮಾತ್ರ ವರದಿ ಮಾಡುತ್ತದೆ.",
        'tbl_td_turnout_prop': "ಮುನ್ಸೂಚಕ ಮತ್ತು ಪ್ರಿಸ್ಕ್ರಿಪ್ಟಿವ್: ಲೈವ್ ಪ್ರಗತಿಶೀಲ ಫಲಿತಾಂಶಗಳನ್ನು ಮುನ್ಸೂಚಿಸುತ್ತದೆ ಮತ್ತು ಮತದಾನ ಮರುಪಡೆಯುವಿಕೆ ಯೋಜನೆಗಳನ್ನು ಶಿಫಾರಸು ಮಾಡುತ್ತದೆ.",
        
        'tbl_td_decision': "ನಿರ್ಧಾರ ಬೆಂಬಲ",
        'tbl_td_decision_exist': "ಯಾವುದೂ ಇಲ್ಲ: ಸ್ಥಿರ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್ ಕೇವಲ ಮೆಟ್ರಿಕ್‌ಗಳನ್ನು ವರದಿ ಮಾಡುತ್ತದೆ.",
        'tbl_td_decision_prop': "ಪ್ರಿಸ್ಕ್ರಿಪ್ಟಿವ್: ಸಮಾಜೋ-ಆರ್ಥಿಕ ಅಡೆತಡೆಗಳ ಆಧಾರದ ಮೇಲೆ ಆಡಳಿತಾತ್ಮಕ ಕಾರ್ಯತಂತ್ರಗಳ ಮ್ಯಾಪಿಂಗ್.",
        
        'tbl_td_sim': "ಕಾರ್ಯಾಚರಣೆಯ ಸಿಮ್ಯುಲೇಟರ್",
        'tbl_td_sim_exist': "ಯಾವುದೂ ಇಲ್ಲ: ಯಾವುದೇ ಸನ್ನಿವೇಶದ ಮೌಲ್ಯಮಾಪನ ಸಾಧ್ಯವಿಲ್ಲ.",
        'tbl_td_sim_prop': "ಸಿಮ್ಯುಲೇಶನ್: ಅಭಿಯಾನಗಳು, ಸಾರಿಗೆ ಶಟಲ್ ಮತ್ತು ಹವಾಮಾನ ಹೊಂದಾಣಿಕೆಗಳ ಪರಿಣಾಮಗಳನ್ನು ಪರೀಕ್ಷಿಸಲು ಲೈವ್ ವಾಟ್-ಇಫ್ ಸ್ಯಾಂಡ್‌ಬಾಕ್ಸ್.",
        
        'tbl_td_risk': "ಅಪಾಯ ಪತ್ತೆಹಚ್ಚುವಿಕೆ",
        'tbl_td_risk_exist': "ಹಸ್ತಚಾಲಿತ: ವಿಶ್ಲೇಷಕರು ಕುಸಿತಗಳನ್ನು ದೃಶ್ಯವಾಗಿ ಪ್ರತ್ಯೇಕಿಸಬೇಕು.",
        'tbl_td_risk_prop': "ಎಐ ರಿಸ್ಕ್ ಡಿಟೆಕ್ಟರ್: ಆರಂಭಿಕ ಎಚ್ಚರಿಕೆಗಳಿಗಾಗಿ ಸ್ವಯಂಚಾಲಿತ ವೈಪರೀತ್ಯ ಎಚ್ಚರಿಕೆಯ ಸೂಚ್ಯಂಕ.",
        
        'tbl_td_relevance': "ಭಾರದ ನಿರ್ದಿಷ್ಟ ಪ್ರಸ್ತುತತೆ",
        'tbl_td_relevance_exist': "ಸಾಮಾನ್ಯ: ಒಟ್ಟಾರೆ ಜಾಗತಿಕ ಜನಸಂಖ್ಯಾ ವೀಕ್ಷಣೆಗಳು.",
        'tbl_td_relevance_prop': "ಲಕ್ಷ್ಯದ: ರಾಜ್ಯ/ಜಿಲ್ಲಾ ಡ್ರಿಲ್‌ಡೌನ್, ಬಹುಭಾಷಾ ಪ್ರಿಸೆಟ್‌ಗಳು ಮತ್ತು ಯುವ ಭಾಗವಹಿಸುವಿಕೆ ಸೂಚ್ಯಂಕ™."
    }
}

def get_layout(lang='en'):
    t = PAGE_TRANSLATIONS.get(lang, PAGE_TRANSLATIONS['en'])
    
    # Comparative Matrix rows
    matrix_rows = [
        html.Tr([
            html.Td(t['tbl_td_turnout'], style={'fontWeight': 'bold'}), 
            html.Td(t['tbl_td_turnout_exist']), 
            html.Td(t['tbl_td_turnout_prop'], style={'color': '#60A5FA', 'fontWeight': '600'})
        ]),
        html.Tr([
            html.Td(t['tbl_td_decision'], style={'fontWeight': 'bold'}), 
            html.Td(t['tbl_td_decision_exist']), 
            html.Td(t['tbl_td_decision_prop'], style={'color': '#60A5FA', 'fontWeight': '600'})
        ]),
        html.Tr([
            html.Td(t['tbl_td_sim'], style={'fontWeight': 'bold'}), 
            html.Td(t['tbl_td_sim_exist']), 
            html.Td(t['tbl_td_sim_prop'], style={'color': '#60A5FA', 'fontWeight': '600'})
        ]),
        html.Tr([
            html.Td(t['tbl_td_risk'], style={'fontWeight': 'bold'}), 
            html.Td(t['tbl_td_risk_exist']), 
            html.Td(t['tbl_td_risk_prop'], style={'color': '#60A5FA', 'fontWeight': '600'})
        ]),
        html.Tr([
            html.Td(t['tbl_td_relevance'], style={'fontWeight': 'bold'}), 
            html.Td(t['tbl_td_relevance_exist']), 
            html.Td(t['tbl_td_relevance_prop'], style={'color': '#60A5FA', 'fontWeight': '600'})
        ])
    ]
    
    comparative_table = dbc.Table([
        html.Thead(html.Tr([
            html.Th(t['tbl_th_audit'], style={'width': '20%'}),
            html.Th(t['tbl_th_existing'], style={'width': '40%'}),
            html.Th(t['tbl_th_proposed'], style={'width': '40%'})
        ]))] + [html.Tbody(matrix_rows)],
        className="table-custom mt-3",
        bordered=False,
        hover=True,
        responsive=True
    )

    return html.Div([
        # Header
        html.Div([
            html.H3(t['title'], style={'fontFamily': 'Poppins', 'fontWeight': '600', 'color': '#F8FAFC'}),
            html.P(t['subtitle'], style={'color': '#94A3B8'})
        ], className="mb-4"),
        
        # Innovation Highlights Card
        dbc.Card([
            html.H5(t['innovation_header'], className="mb-3", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
            html.P([
                t['innovation_p1'], html.Strong(t['innovation_p2'], style={'color': '#94A3B8'}), 
                t['innovation_p3'],
                html.Span(t['innovation_p4'], style={'fontWeight': '700', 'color': '#2563EB'}), 
                t['innovation_p5'], html.Strong(t['innovation_p6'], style={'color': '#60A5FA'}), 
                t['innovation_p7'], html.Strong(t['innovation_p8'], style={'color': '#22C55E'}), 
                t['innovation_p9']
            ], style={'fontSize': '0.9rem', 'lineHeight': '1.5', 'color': '#E2E8F0', 'margin': 0})
        ], className="stat-card p-4 mb-4"),
        
        # Creator Profile & Core Features Card
        dbc.Card([
            dbc.Row([
                dbc.Col([
                    html.H5(t['creator_header'], className="mb-3", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
                    html.Div([
                        html.Div([
                            html.Div(t['creator_name'], style={'fontSize': '1.3rem', 'fontWeight': 'bold', 'color': '#60A5FA', 'fontFamily': 'Poppins'}),
                            html.Div(t['creator_role'], style={'fontSize': '0.85rem', 'color': '#94A3B8', 'fontWeight': '500', 'textTransform': 'uppercase', 'letterSpacing': '0.05em'})
                        ], className="mb-3"),
                        html.P(t['creator_desc'], 
                               style={'fontSize': '0.85rem', 'lineHeight': '1.5', 'color': '#E2E8F0'}),
                        html.Div([
                            html.Span(t['badge_python'], className="badge bg-secondary me-2", style={'fontSize': '0.75rem'}),
                            html.Span(t['badge_scikit'], className="badge bg-secondary me-2", style={'fontSize': '0.75rem'}),
                            html.Span(t['badge_data_viz'], className="badge bg-secondary", style={'fontSize': '0.75rem'})
                        ], className="mt-3")
                    ])
                ], lg=5, md=12, className="border-end border-secondary pe-lg-4 mb-4 mb-lg-0"),
                
                dbc.Col([
                    html.H5(t['features_header'], className="mb-3", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
                    dbc.Row([
                        dbc.Col([
                            html.Ul([
                                html.Li([html.Strong(t['feat_pulse_lbl']), t['feat_pulse_val']], style={'fontSize': '0.8rem', 'color': '#E2E8F0', 'marginBottom': '0.5rem'}),
                                html.Li([html.Strong(t['feat_forecast_lbl']), t['feat_forecast_val']], style={'fontSize': '0.8rem', 'color': '#E2E8F0', 'marginBottom': '0.5rem'}),
                                html.Li([html.Strong(t['feat_xai_lbl']), t['feat_xai_val']], style={'fontSize': '0.8rem', 'color': '#E2E8F0'})
                            ], className="ps-3 mb-3 mb-md-0")
                        ], md=6),
                        dbc.Col([
                            html.Ul([
                                html.Li([html.Strong(t['feat_sim_lbl']), t['feat_sim_val']], style={'fontSize': '0.8rem', 'color': '#E2E8F0', 'marginBottom': '0.5rem'}),
                                html.Li([html.Strong(t['feat_advisor_lbl']), t['feat_advisor_val']], style={'fontSize': '0.8rem', 'color': '#E2E8F0', 'marginBottom': '0.5rem'}),
                                html.Li([html.Strong(t['feat_risk_lbl']), t['feat_risk_val']], style={'fontSize': '0.8rem', 'color': '#E2E8F0'})
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
                    html.H5(t['formulas_header'], className="mb-4", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
                    
                    html.Div([
                        html.H6(t['formula_pulse_lbl'], style={'fontWeight': '600', 'color': '#60A5FA'}),
                        html.P(t['formula_pulse_desc'], style={'fontSize': '0.8rem', 'color': '#94A3B8'}),
                        html.Code(
                            "Pulse = 0.6*Turnout_Forecast + 0.3*EHS_Avg + 0.1*(1 - High_Risk_Ratio)*100",
                            style={'backgroundColor': '#0F1626', 'padding': '0.5rem 1rem', 'borderRadius': '4px', 'display': 'block', 'color': '#4ADE80', 'fontSize': '0.75rem', 'fontFamily': 'monospace'}
                        ),
                    ], className="mb-4"),
                    
                    html.Div([
                        html.H6(t['formula_ehs_lbl'], style={'fontWeight': '600', 'color': '#60A5FA'}),
                        html.P(t['formula_ehs_desc'], style={'fontSize': '0.8rem', 'color': '#94A3B8'}),
                        html.Code(
                            "EHS = 0.4*Turnout + 0.2*Awareness + 0.15*Accessibility + 0.15*MomentumFactor - 0.1*RiskPenalty",
                            style={'backgroundColor': '#0F1626', 'padding': '0.5rem 1rem', 'borderRadius': '4px', 'display': 'block', 'color': '#4ADE80', 'fontSize': '0.75rem', 'fontFamily': 'monospace'}
                        ),
                        html.Ul([
                            html.Li(t['formula_ehs_note1'], style={'fontSize': '0.75rem', 'marginTop': '0.3rem', 'color': '#94A3B8'}),
                            html.Li(t['formula_ehs_note2'], style={'fontSize': '0.75rem', 'color': '#94A3B8'})
                        ], className="ps-3 mt-1")
                    ], className="mb-4"),
                    
                    html.Div([
                        html.H6(t['formula_cis_lbl'], style={'fontWeight': '600', 'color': '#60A5FA'}),
                        html.P(t['formula_cis_desc'], style={'fontSize': '0.8rem', 'color': '#94A3B8'}),
                        html.Code(
                            "CIS = 0.45*Turnout + 0.25*Awareness + 0.20*Accessibility + 0.10*MomentumFactor",
                            style={'backgroundColor': '#0F1626', 'padding': '0.5rem 1rem', 'borderRadius': '4px', 'display': 'block', 'color': '#4ADE80', 'fontSize': '0.75rem', 'fontFamily': 'monospace'}
                        )
                    ], className="mb-4"),
                    
                    html.Div([
                        html.H6(t['formula_ypi_lbl'], style={'fontWeight': '600', 'color': '#60A5FA'}),
                        html.P(t['formula_ypi_desc'], style={'fontSize': '0.8rem', 'color': '#94A3B8'}),
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
                    html.H5(t['ml_header'], className="mb-4", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
                    
                    html.Div([
                        html.H6(t['ml_xai_lbl'], style={'fontWeight': '600', 'color': '#60A5FA'}),
                        html.P(t['ml_xai_desc'], style={'fontSize': '0.8rem', 'color': '#94A3B8'}),
                    ], className="mb-3"),
                    
                    html.Div([
                        html.H6(t['ml_rf_lbl'], style={'fontWeight': '600', 'color': '#60A5FA'}),
                        html.P(t['ml_rf_desc'], style={'fontSize': '0.8rem', 'color': '#94A3B8'}),
                    ], className="mb-4"),
                    
                    html.H6(t['tech_header'], style={'fontWeight': '600', 'color': '#F8FAFC', 'marginBottom': '0.6rem'}),
                    html.Ul([
                        html.Li(t['tech_item_1'], style={'fontSize': '0.8rem', 'color': '#94A3B8', 'marginBottom': '0.2rem'}),
                        html.Li(t['tech_item_2'], style={'fontSize': '0.8rem', 'color': '#94A3B8', 'marginBottom': '0.2rem'}),
                        html.Li(t['tech_item_3'], style={'fontSize': '0.8rem', 'color': '#94A3B8', 'marginBottom': '0.2rem'}),
                        html.Li(t['tech_item_4'], style={'fontSize': '0.8rem', 'color': '#94A3B8'})
                    ], className="ps-3 mb-4"),
                    
                    # Ethical disclosure banner
                    html.Div([
                        html.Div(t['disclaimer_title'], style={'fontWeight': '700', 'color': '#EF4444', 'fontSize': '0.85rem', 'marginBottom': '0.4rem'}),
                        html.P(
                            t['disclaimer_desc'],
                            style={'fontSize': '0.75rem', 'color': '#FCA5A5', 'margin': 0, 'lineHeight': '1.3'}
                        )
                    ], className="custom-alert p-3 rounded active-pulse", style={'border': '1px solid rgba(239, 68, 68, 0.3)'})
                ], className="stat-card p-4")
            ], lg=6, md=12)
        ]),
        
        # Comparative Matrix card
        dbc.Card([
            html.H5(t['tbl_header_matrix'], className="mb-3", style={'fontFamily': 'Poppins', 'color': '#F8FAFC'}),
            html.P(t['tbl_header_matrix_desc'], style={'fontSize': '0.85rem', 'color': '#94A3B8'}),
            comparative_table
        ], className="stat-card p-4 mb-4")
    ])
