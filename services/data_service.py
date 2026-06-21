import pandas as pd
import numpy as np
import os
import sys
import joblib
import json

# Ensure parent directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class DataService:
    def __init__(self):
        self.df = None
        self.reg_model = None
        self.clf_model = None
        self.model_eval = None
        self.load_data()
        self.load_models()

    def load_data(self):
        """Loads dataset and adds calculated properties."""
        if os.path.exists(config.DATASET_PATH):
            self.df = pd.read_csv(config.DATASET_PATH)
            # Pre-calculate scores if they aren't explicitly saved
            self.df['is_urban'] = self.df['region_type'].map({'Urban': 1, 'Rural': 0}).fillna(0).astype(int)
            self._enrich_data()
        else:
            self.df = pd.DataFrame()

    def load_models(self):
        """Loads pre-trained Random Forest models and evaluation details."""
        if os.path.exists(config.TURNOUT_MODEL_PATH):
            self.reg_model = joblib.load(config.TURNOUT_MODEL_PATH)
        if os.path.exists(config.RISK_MODEL_PATH):
            self.clf_model = joblib.load(config.RISK_MODEL_PATH)
            
        eval_path = os.path.join(config.TRAINED_MODELS_DIR, 'model_evaluation.json')
        if os.path.exists(eval_path):
            with open(eval_path, 'r') as f:
                self.model_eval = json.load(f)

    def _enrich_data(self):
        """Computes custom metrics (Health Score, Civic Impact Score, Youth Index) for the dataset."""
        health_scores = []
        civic_impact_scores = []
        youth_turnout_scores = []
        
        for idx, row in self.df.iterrows():
            # Extract attributes
            turnout = row['current_turnout']
            awareness = row['awareness_score']
            accessibility = row['transport_accessibility']
            momentum = row['participation_momentum']
            risk = row['risk_level']
            final_turnout = row['actual_final_turnout']
            
            # 1. Health Score calculation
            h_score = self.calculate_health_score(turnout, awareness, accessibility, momentum, risk)
            health_scores.append(h_score)
            
            # 2. Civic Impact Score calculation
            c_score = self.calculate_civic_impact_score(turnout, awareness, accessibility, momentum)
            civic_impact_scores.append(c_score)
            
            # 3. Youth Participation Index calculation
            # Youth turnout modeled with urban apathy factors and awareness correlation
            y_turnout = final_turnout * 0.91 * (awareness / 72.0)
            # Clip between reasonable bounds
            y_turnout = max(40.0, min(95.0, y_turnout))
            youth_turnout_scores.append(round(y_turnout, 1))
            
        self.df['election_health_score'] = health_scores
        self.df['civic_impact_score'] = civic_impact_scores
        self.df['youth_turnout_sim'] = youth_turnout_scores

    @staticmethod
    def calculate_health_score(turnout, awareness, accessibility, momentum, risk):
        """Election Health Score (EHS)™ logic."""
        momentum_factor = 100 if momentum == 'Accelerating' else (75 if momentum == 'Stable' else 50)
        risk_penalty = 100 if risk == 'High' else (50 if risk == 'Medium' else 0)
        
        # Formula: 40% Turnout + 20% Awareness + 15% Accessibility + 15% Momentum - 10% Risk
        score = (0.4 * turnout + 
                 0.2 * awareness + 
                 0.15 * accessibility + 
                 0.15 * momentum_factor - 
                 0.1 * risk_penalty)
        return round(max(0.0, min(100.0, score)), 1)

    @staticmethod
    def calculate_civic_impact_score(turnout, awareness, accessibility, momentum):
        """Civic Impact Score™ logic."""
        momentum_factor = 100 if momentum == 'Accelerating' else (75 if momentum == 'Stable' else 50)
        
        # Formula: 45% Turnout + 25% Awareness + 20% Accessibility + 10% Momentum
        score = (0.45 * turnout + 
                 0.25 * awareness + 
                 0.20 * accessibility + 
                 0.10 * momentum_factor)
        return round(max(0.0, min(100.0, score)), 1)

    def get_national_stats(self):
        """Aggregates overview stats for the Landing Dashboard, including new Pulse & Youth Index."""
        if self.df.empty:
            return {}
        
        total_registered = int(self.df['registered_voters'].sum())
        avg_current_turnout = float(self.df['current_turnout'].mean())
        
        # Dynamically predict final turnout for all rows
        if self.reg_model is not None:
            features = self.df[[
                'historical_turnout', 'literacy_rate', 'awareness_score', 
                'transport_accessibility', 'weather_score', 'campaign_intensity', 
                'holiday_factor', 'is_urban'
            ]]
            self.df['predicted_final_turnout'] = self.reg_model.predict(features)
            avg_predicted_turnout = float(self.df['predicted_final_turnout'].mean())
        else:
            avg_predicted_turnout = float(self.df['actual_final_turnout'].mean())
            
        avg_health = float(self.df['election_health_score'].mean())
        high_risk_count = int((self.df['risk_level'] == 'High').sum())
        medium_risk_count = int((self.df['risk_level'] == 'Medium').sum())
        
        # Active Alerts simulation
        alerts_count = high_risk_count + int(medium_risk_count / 2)
        
        # 1. National Election Pulse™ Calculation
        # Pulse is based on average expected final turnout, health index, and risk minimization
        high_risk_ratio = high_risk_count / len(self.df)
        pulse = 0.6 * avg_predicted_turnout + 0.3 * avg_health + 0.1 * (1.0 - high_risk_ratio) * 100
        pulse_score = round(max(0.0, min(100.0, pulse)), 1)
        
        if pulse_score >= 80.0:
            pulse_status = "Healthy Participation Trend"
        elif pulse_score >= 70.0:
            pulse_status = "Stable Participation Corridor"
        else:
            pulse_status = "Weak voter turnout warning"
            
        # 2. Youth Participation Index™ Calculation
        avg_youth_turnout = float(self.df['youth_turnout_sim'].mean())
        ypi_score = round(avg_youth_turnout, 1)
        
        if ypi_score >= 75.0:
            ypi_status = "Strong Youth Engagement"
        elif ypi_score >= 65.0:
            ypi_status = "Moderate Youth Engagement"
        else:
            ypi_status = "High Youth Apathy Alert"
            
        return {
            'total_regions': len(self.df),
            'registered_voters': total_registered,
            'current_turnout': round(avg_current_turnout, 2),
            'predicted_turnout': round(avg_predicted_turnout, 2),
            'health_score': round(avg_health, 1),
            'high_risk_zones': high_risk_count,
            'active_alerts': alerts_count,
            
            # Upgraded metrics
            'pulse_score': pulse_score,
            'pulse_status': pulse_status,
            'ypi_score': ypi_score,
            'ypi_status': ypi_status
        }

    def filter_data(self, state=None, district=None, risk_level=None, region_type=None, search_query=None):
        """Filters dataset based on parameters."""
        if self.df.empty:
            return self.df
            
        filtered = self.df.copy()
        
        if state and state != 'ALL':
            filtered = filtered[filtered['state'] == state]
        if district and district != 'ALL':
            filtered = filtered[filtered['district'] == district]
        if risk_level and risk_level != 'ALL':
            filtered = filtered[filtered['risk_level'] == risk_level]
        if region_type and region_type != 'ALL':
            filtered = filtered[filtered['region_type'] == region_type]
            
        if search_query:
            q = search_query.lower()
            filtered = filtered[
                filtered['constituency'].str.lower().str.contains(q) |
                filtered['district'].str.lower().str.contains(q) |
                filtered['state'].str.lower().str.contains(q)
            ]
            
        return filtered

    def get_states(self):
        """Returns sorted list of distinct states."""
        if self.df.empty:
            return []
        return sorted(self.df['state'].unique().tolist())

    def get_districts(self, state=None):
        """Returns sorted list of distinct districts, optionally filtered by state."""
        if self.df.empty:
            return []
        if state and state != 'ALL':
            return sorted(self.df[self.df['state'] == state]['district'].unique().tolist())
        return sorted(self.df['district'].unique().tolist())

    def get_constituencies(self, state=None, district=None):
        """Returns sorted list of constituencies, optionally filtered."""
        if self.df.empty:
            return []
        temp = self.df.copy()
        if state and state != 'ALL':
            temp = temp[temp['state'] == state]
        if district and district != 'ALL':
            temp = temp[temp['district'] == district]
        return sorted(temp['constituency'].unique().tolist())

    def predict_region(self, historical_turnout, literacy_rate, awareness_score, 
                       transport_accessibility, weather_score, campaign_intensity, 
                       holiday_factor, region_type):
        """Runs the machine learning models and returns turnout, risk, confidence, AND explainable AI drivers."""
        is_urban = 1 if region_type == 'Urban' else 0
        
        # Predict Turnout & Risk
        if self.reg_model is None or self.clf_model is None:
            # Simple fallback model if ML file is missing
            pred_turnout = historical_turnout + (awareness_score - 60) * 0.1 + (weather_score - 70) * 0.05
            pred_turnout = max(40.0, min(95.0, pred_turnout))
            risk_label = 'Low' if pred_turnout > historical_turnout - 2 else 'Medium'
            confidence = 85.0
        else:
            input_data = pd.DataFrame([{
                'historical_turnout': float(historical_turnout),
                'literacy_rate': float(literacy_rate),
                'awareness_score': float(awareness_score),
                'transport_accessibility': float(transport_accessibility),
                'weather_score': float(weather_score),
                'campaign_intensity': float(campaign_intensity),
                'holiday_factor': int(holiday_factor),
                'is_urban': is_urban
            }])
            
            # Regressor prediction
            pred_turnout = self.reg_model.predict(input_data)[0]
            
            # Classifier prediction
            pred_risk_idx = self.clf_model.predict(input_data)[0]
            risk_labels = ['Low', 'Medium', 'High']
            risk_label = risk_labels[pred_risk_idx]
            
            # Confidence logic
            probs = self.clf_model.predict_proba(input_data)[0]
            max_prob = max(probs)
            confidence = round(70.0 + (max_prob * 28.0), 1)

        # 3. Explainable AI (XAI) feature contribution drivers calculation
        # Baseline is the historical average baseline
        baseline = 68.50
        
        # Compute exact impact scores matching our data generator weights
        lit_contrib = 0.05 * (float(literacy_rate) - 75.0)
        aware_contrib = 0.10 * (float(awareness_score) - 60.0)
        trans_contrib = 0.06 * (float(transport_accessibility) - 70.0)
        weather_contrib = 0.08 * (float(weather_score) - 70.0)
        camp_contrib = 0.12 * (float(campaign_intensity) - 50.0)
        holiday_contrib = -3.50 * int(holiday_factor)
        density_contrib = -1.50 if is_urban == 1 else 1.00
        
        # Balance out residual to ensure mathematical consistency with model output
        sum_contribs = (historical_turnout - baseline) + lit_contrib + aware_contrib + trans_contrib + weather_contrib + camp_contrib + holiday_contrib + density_contrib
        residual = pred_turnout - (baseline + sum_contribs)
        
        drivers = [
            {"feature": "Historical Regional Baseline", "contribution": round(historical_turnout, 2), "type": "baseline"},
            {"feature": "Literacy Level Deviation", "contribution": round(lit_contrib, 2), "type": "demographic"},
            {"feature": "Awareness Campaign Impact", "contribution": round(aware_contrib, 2), "type": "outreach"},
            {"feature": "Booth Access Infrastructure", "contribution": round(trans_contrib, 2), "type": "infrastructure"},
            {"feature": "Weather Comfort Index", "contribution": round(weather_contrib, 2), "type": "environmental"},
            {"feature": "Political Campaign Density", "contribution": round(camp_contrib, 2), "type": "political"},
            {"feature": "Holiday Drag Factor", "contribution": round(holiday_contrib, 2), "type": "environmental"},
            {"feature": "Urban/Rural Density Delta", "contribution": round(density_contrib, 2), "type": "demographic"},
            {"feature": "Interactive Model Adjustments", "contribution": round(residual, 2), "type": "model_adjust"}
        ]
        
        return round(pred_turnout, 2), risk_label, confidence, drivers

    def get_live_feed(self):
        """Generates dynamic AI Insight Feed™ reports simulating real-time anomalies and prescriptions."""
        if self.df.empty:
            return []
            
        feed = [
            {"time": "09:00 AM", "message": "AI Diagnostics: National voter registration audited. Overall youth registry is at 31.4%.", "type": "info"},
        ]
        
        # Locate high-risk areas dynamically and generate verbose insights
        high_risk_rows = self.df[self.df['risk_level'] == 'High']
        if not high_risk_rows.empty:
            for idx, row in high_risk_rows.head(2).iterrows():
                deficit = row['historical_turnout'] - row['current_turnout']
                suggested_lift = round((100 - row['awareness_score']) * 0.14, 1)
                feed.append({
                    "time": "AI INSIGHT",
                    "message": f"Critical Underperformance Alert: {row['constituency']} ({row['state']}) turnout is {deficit:.1f}% below target. Primary issue: Low local campaigning. Deploying outreach could lift turnout by +{suggested_lift}%.",
                    "type": "danger"
                })
        
        # Add transport gap alert
        low_access_rows = self.df[self.df['transport_accessibility'] < 55]
        if not low_access_rows.empty:
            r = low_access_rows.iloc[0]
            feed.append({
                "time": "AI INSIGHT",
                "message": f"Infrastructure Barrier: Transport accessibility deficit detected in {r['constituency']} ({r['district']}). Deploying election day shuttle buses is expected to secure a +4.2% turnout lift.",
                "type": "warning"
            })
            
        feed.append({"time": "02:00 PM", "message": "Weather Station Update: Heatwave warnings in southern sectors resolved. Voter throughput stabilized.", "type": "success"})
        
        return feed

    def get_interventions(self, state=None, limit=10):
        """Generates sorted action recommendations for the Election Strategy Advisor™."""
        data = self.df.copy()
        if state and state != 'ALL':
            data = data[data['state'] == state]
            
        recommendations = []
        for idx, row in data.iterrows():
            turnout = row['current_turnout']
            awareness = row['awareness_score']
            accessibility = row['transport_accessibility']
            weather = row['weather_score']
            youth_ratio = row['youth_voters'] / row['registered_voters']
            
            # Diagnose primary problems, action recipes, expected gains, and difficulty
            primary_problem = "General Voter Apathy"
            action = "Deploy Door-to-Door Information Volunteers"
            lift_gain = "+3.5% Turnout"
            difficulty = "Easy"
            
            if turnout < 55 and awareness < 60:
                primary_problem = "Low Civic Awareness"
                action = "Deploy Multilingual Audio Van Campaigns"
                lift_gain = "+5.8% Turnout"
                difficulty = "Medium"
            elif accessibility < 60:
                primary_problem = "Transportation Access Gaps"
                action = "Deploy Free Polling Station Shuttle Fleet"
                lift_gain = "+4.6% Turnout"
                difficulty = "Easy"
            elif weather < 50:
                primary_problem = "Severe Weather Drag"
                action = "Erect Cooling Tents, Shaded Queues & Water Stations"
                lift_gain = "+3.2% Turnout"
                difficulty = "Easy"
            elif youth_ratio > 0.30 and turnout < 60:
                primary_problem = "Low Youth Engagement"
                action = "Launch College Campus Rallies & Social Voting Challenges"
                lift_gain = "+5.4% Turnout"
                difficulty = "Medium"
                
            actions = [{
                "action": action,
                "reason": f"Deficit mapped to {primary_problem.lower()} metrics.",
                "impact": lift_gain,
                "difficulty": difficulty
            }]
            
            # Fallback secondary action
            if primary_problem != "General Voter Apathy":
                actions.append({
                    "action": "Broadcast Localized SMS Broadcast Notifications",
                    "reason": "Secondary reinforcement channel to boost participation.",
                    "impact": "+1.8% Turnout",
                    "difficulty": "Easy"
                })
            else:
                actions.append({
                    "action": "Maintain Standard Voter Pamphlet Distribution",
                    "reason": "Reinforce standard voting booths location mapping.",
                    "impact": "+1.0% Turnout",
                    "difficulty": "Easy"
                })
            
            # Priority rank calculation
            deficit = row['historical_turnout'] - turnout
            priority_score = deficit + (100 - awareness) * 0.25
            
            recommendations.append({
                "constituency": row['constituency'],
                "district": row['district'],
                "state": row['state'],
                "risk_level": row['risk_level'],
                "current_turnout": turnout,
                "historical_turnout": row['historical_turnout'],
                "priority_score": priority_score,
                "primary_issue": primary_problem,
                "actions": actions
            })
            
        # Sort by priority score descending
        recommendations = sorted(recommendations, key=lambda x: x['priority_score'], reverse=True)
        return recommendations[:limit]
