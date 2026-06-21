import pandas as pd
import numpy as np
import os
import sys
import json
import urllib.request

# Ensure parent directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

JSON_URL = "https://raw.githubusercontent.com/sab99r/Indian-States-And-Districts/master/states-and-districts.json"
LOCAL_JSON_PATH = os.path.join(config.DATA_DIR, "states-and-districts.json")

def load_states_and_districts():
    """Fetches the complete states and districts list from GitHub and caches it locally."""
    # Try fetching from remote URL
    try:
        print(f"Fetching complete states and districts from: {JSON_URL}...")
        req = urllib.request.Request(
            JSON_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
        # Cache locally
        with open(LOCAL_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print("Successfully cached states and districts JSON locally.")
        return data
    except Exception as e:
        print(f"Remote fetch failed ({str(e)}). Attempting to load from local cache...")
        
    # Check if local cache exists
    if os.path.exists(LOCAL_JSON_PATH):
        try:
            with open(LOCAL_JSON_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print("Loaded states and districts from local cache.")
            return data
        except Exception as e:
            print(f"Failed to read local cache JSON ({str(e)}).")
            
    # Fallback minimal hardcoded dictionary in case of complete connection failure
    print("WARNING: Falling back to minimal geo structure.")
    return {
        "states": [
            {
                "state": "Karnataka",
                "districts": ["Bengaluru Urban", "Mysuru", "Belagavi", "Kalaburagi", "Raichur", "Dharwad", "Mangaluru"]
            },
            {
                "state": "Maharashtra",
                "districts": ["Mumbai City", "Pune", "Nagpur", "Nashik", "Aurangabad", "Thane"]
            }
        ]
    }

def generate_synthetic_data():
    np.random.seed(42)
    
    geo_data = load_states_and_districts()
    states_list = geo_data.get('states', [])
    
    rows = []
    
    # Loop over every single state/UT and every district from the JSON mapping
    for state_item in states_list:
        state_name = state_item.get('state')
        districts = state_item.get('districts', [])
        
        # State-specific characteristics baseline
        if 'Kerala' in state_name:
            state_literacy_baseline = 94.0
            state_turnout_baseline = 75.0
        elif 'Bihar' in state_name or 'Uttar Pradesh' in state_name:
            state_literacy_baseline = 68.0
            state_turnout_baseline = 61.0
        else:
            state_literacy_baseline = 76.0
            state_turnout_baseline = 68.0
            
        for district in districts:
            # Clean names and strings
            district = district.strip()
            # Constituency name
            constituency = f"{district} Assembly"
            
            # Region Type (Urban vs Rural)
            is_urban = any(keyword in district.lower() for keyword in [
                'city', 'urban', 'metropolitan', 'central', 'east', 'west', 
                'north', 'south', 'mumbai', 'delhi', 'chennai', 'kolkata', 'hyderabad', 'bengaluru', 'pune'
            ])
            region_type = 'Urban' if is_urban or np.random.rand() > 0.72 else 'Rural'
            
            # Demographics
            population = int(np.random.randint(180000, 650000))
            registered_ratio = np.random.uniform(0.60, 0.74)
            registered_voters = int(population * registered_ratio)
            
            female_ratio = np.random.uniform(0.46, 0.495)
            female_voters = int(registered_voters * female_ratio)
            male_voters = registered_voters - female_voters
            
            youth_ratio = np.random.uniform(0.24, 0.38)
            youth_voters = int(registered_voters * youth_ratio)
            senior_ratio = np.random.uniform(0.09, 0.15)
            senior_voters = int(registered_voters * senior_ratio)
            
            # Literacy
            lit_delta = np.random.uniform(-8, 8) + (5 if region_type == 'Urban' else -5)
            literacy_rate = round(clip(state_literacy_baseline + lit_delta, 42.0, 99.0), 2)
            
            # Infrastructure and Awareness
            transport_accessibility = int(clip(np.random.normal(70, 11) + (8 if region_type == 'Urban' else -8), 30, 98))
            awareness_score = int(clip(np.random.normal(68, 9) + (4 if region_type == 'Urban' else -2), 35, 98))
            
            # Environmental
            weather_score = int(clip(np.random.normal(74, 14), 20, 98))
            campaign_intensity = int(clip(np.random.normal(62, 14), 20, 98))
            holiday_factor = 1 if np.random.rand() > 0.85 else 0
            
            # Historical Turnout
            hist_delta = np.random.normal(0, 4) + (2.5 if region_type == 'Rural' else -2.5)
            historical_turnout = round(clip(state_turnout_baseline + hist_delta, 46.0, 89.0), 2)
            
            # Calculate final turnout
            weather_impact = (weather_score - 70) * 0.08
            awareness_impact = (awareness_score - 60) * 0.06
            transport_impact = (transport_accessibility - 70) * 0.05
            campaign_impact = (campaign_intensity - 50) * 0.08
            holiday_impact = -4.2 if holiday_factor == 1 else 0.0
            density_impact = -1.5 if region_type == 'Urban' else 1.0
            
            final_turnout_val = historical_turnout + weather_impact + awareness_impact + transport_impact + campaign_impact + holiday_impact + density_impact
            final_turnout_val += np.random.normal(0, 1.8)
            final_turnout = round(clip(final_turnout_val, 40.0, 92.0), 2)
            
            # Progression percentages per hour
            p_9am = np.random.uniform(0.18, 0.24)
            p_11am = np.random.uniform(0.40, 0.46)
            p_1pm = np.random.uniform(0.58, 0.65)
            p_3pm = np.random.uniform(0.75, 0.82)
            p_5pm = np.random.uniform(0.90, 0.96)
            
            turnout_9am = round(final_turnout * p_9am, 2)
            turnout_11am = round(final_turnout * p_11am, 2)
            turnout_1pm = round(final_turnout * p_1pm, 2)
            turnout_3pm = round(final_turnout * p_3pm, 2)
            turnout_5pm = round(final_turnout * p_5pm, 2)
            
            current_turnout = turnout_3pm
            
            # Momentum
            morning_rate = turnout_11am - turnout_9am
            afternoon_rate = turnout_3pm - turnout_1pm
            momentum_diff = afternoon_rate - morning_rate
            
            if momentum_diff > 1.5:
                momentum = 'Accelerating'
            elif momentum_diff < -1.5:
                momentum = 'Declining'
            else:
                momentum = 'Stable'
                
            # Risk Level
            expected_3pm_from_hist = historical_turnout * 0.78
            turnout_deficit = expected_3pm_from_hist - current_turnout
            
            if turnout_deficit > 4.0 or (final_turnout < historical_turnout - 5.0):
                risk_level = 'High'
            elif turnout_deficit > 1.5 or (final_turnout < historical_turnout - 2.0):
                risk_level = 'Medium'
            else:
                risk_level = 'Low'
                
            rows.append({
                'state': state_name,
                'district': district,
                'constituency': constituency,
                'constituency_hi': constituency,  # Fallback for translation columns
                'constituency_kn': constituency,
                'region_type': region_type,
                'population': population,
                'registered_voters': registered_voters,
                'male_voters': male_voters,
                'female_voters': female_voters,
                'youth_voters': youth_voters,
                'senior_voters': senior_voters,
                'literacy_rate': literacy_rate,
                'transport_accessibility': transport_accessibility,
                'awareness_score': awareness_score,
                'weather_score': weather_score,
                'campaign_intensity': campaign_intensity,
                'holiday_factor': holiday_factor,
                'historical_turnout': historical_turnout,
                'turnout_9am': turnout_9am,
                'turnout_11am': turnout_11am,
                'turnout_1pm': turnout_1pm,
                'turnout_3pm': turnout_3pm,
                'turnout_5pm': turnout_5pm,
                'current_turnout': current_turnout,
                'participation_momentum': momentum,
                'risk_level': risk_level,
                'actual_final_turnout': final_turnout
            })
            
    df = pd.DataFrame(rows)
    df.to_csv(config.DATASET_PATH, index=False)
    print(f"SUCCESS: Generated {len(df)} records covering ALL Indian states & districts.")
    return df

def clip(val, min_val, max_val):
    return max(min_val, min(max_val, val))

if __name__ == '__main__':
    generate_synthetic_data()
