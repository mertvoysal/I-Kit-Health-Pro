import os
if os.name == "nt":
    # Work around Windows WMI stalls observed during pandas startup.
    import platform
    _arch = os.environ.get("PROCESSOR_ARCHITECTURE", "AMD64")
    _system = os.environ.get("OS", "Windows_NT").replace("_NT", "")
    platform.machine = lambda: _arch
    platform.system = lambda: _system

from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import json
import math
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from catboost import CatBoostClassifier
import warnings

warnings.filterwarnings("ignore")

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.auto_reload = True

df = pd.read_csv('thyroidDF.csv') 
df = df.drop(['TBG', 'patient_id'], axis=1)

def fix_target(value):
    letter = str(value)[0].upper()
    if letter in ['A', 'B', 'C', 'D']: return 0 
    elif letter in ['E', 'F', 'G', 'H']: return 1 
    else: return 2 

df['target'] = df['target'].apply(fix_target)

for col in ['TSH', 'T3', 'TT4', 'T4U', 'FTI']:
    df[col] = df[col].fillna(df[col].median())
df['sex'] = df['sex'].fillna(df['sex'].mode()[0])

le = LabelEncoder()
categorical_columns = df.select_dtypes(include=['object']).columns
for col in categorical_columns:
    df[col] = df[col].astype(str)
    df[col] = le.fit_transform(df[col])

X = df.drop('target', axis=1)
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

MODEL_DIR = "artifacts"
MODEL_PATH = os.path.join(MODEL_DIR, "catboost_thyroid_model.cbm")
MODEL_METADATA_PATH = os.path.join(MODEL_DIR, "model_metadata.json")
MODEL_VERSION = "1.0.0"
DISCLAIMER_TEXT = "This system does not provide a medical diagnosis; it is a clinical decision-support tool to assist physicians."
model_metadata = {}

def _utc_now_iso():
    return datetime.now(timezone.utc).isoformat()

def _write_model_metadata(metadata):
    os.makedirs(MODEL_DIR, exist_ok=True)
    with open(MODEL_METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

def _read_model_metadata():
    if not os.path.exists(MODEL_METADATA_PATH):
        return None
    try:
        with open(MODEL_METADATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

def load_or_train_model():
    global model_metadata
    model = CatBoostClassifier(verbose=0, random_state=42)
    if os.path.exists(MODEL_PATH):
        model.load_model(MODEL_PATH)
        model_metadata = _read_model_metadata()
        if not model_metadata:
            model_metadata = {
                "model_version": MODEL_VERSION,
                "trained_at": None,
                "loaded_from_disk": True
            }
            _write_model_metadata(model_metadata)
        model_metadata["loaded_from_disk"] = True
        return model

    model.fit(X_train, y_train)
    os.makedirs(MODEL_DIR, exist_ok=True)
    model.save_model(MODEL_PATH)
    model_metadata = {
        "model_version": MODEL_VERSION,
        "trained_at": _utc_now_iso(),
        "loaded_from_disk": False
    }
    _write_model_metadata(model_metadata)
    return model

catboost_model = load_or_train_model()

hospitals = [
    'Ege University Hospital', 'Tepecik Training and Research Hospital', 
    'Alsancak Nevvar Salih Isgoren State Hospital', 'Izmir City Hospital', 
    'Dokuz Eylul Hospital', 'Cigli Training and Research State Hospital'
]
hospital_coordinates = {
    'Ege University Hospital': (38.4566942, 27.2099364),
    'Tepecik Training and Research Hospital': (38.4230722, 27.1659604),
    'Alsancak Nevvar Salih Isgoren State Hospital': (38.4343139, 27.1430765),
    'Izmir City Hospital': (38.4848619, 27.1784716),
    'Dokuz Eylul Hospital': (38.3947268, 27.0323447),
    'Cigli Training and Research State Hospital': (38.4998565, 27.0494967)
}
hospital_map_urls = {
    'Izmir City Hospital': 'https://www.google.com/maps/place/%C4%B0zmir+%C5%9Eehir+Hastanesi/@44.8869346,-25.0364219,3z/data=!4m6!3m5!1s0x14bbd7dfa8802361:0xc19f1597aa3ffd81!8m2!3d38.4848619!4d27.1784716!16s%2Fg%2F11flgqgrsc?entry=ttu&g_ep=EgoyMDI2MDQxMy4wIKXMDSoASAFQAw%3D%3D',
    'Ege University Hospital': 'https://www.google.com/maps/place/Ege+%C3%9Cniversitesi+T%C4%B1p+Fak%C3%BCltesi+Hastanesi/@44.8869346,-25.0364219,3z/data=!4m6!3m5!1s0x14b97d25a63c5665:0x1254f127dfa9fbf9!8m2!3d38.4566942!4d27.2099364!16s%2Fg%2F1x5bblkm?entry=ttu&g_ep=EgoyMDI2MDQxMy4wIKXMDSoASAFQAw%3D%3D',
    'Tepecik Training and Research Hospital': 'https://www.google.com/maps/place/%C4%B0zmir+Tepecik+E%C4%9Fitim+Ara%C5%9Ft%C4%B1rma+Hastanesi/@38.4230722,27.1659604,17z/data=!3m1!4b1!4m6!3m5!1s0x14bbd887ea422985:0x22b5ad1c637eb863!8m2!3d38.4230722!4d27.1659604!16s%2Fg%2F1tfn_slz?entry=ttu&g_ep=EgoyMDI2MDQxMy4wIKXMDSoASAFQAw%3D%3D',
    'Alsancak Nevvar Salih Isgoren State Hospital': 'https://www.google.com/maps/place/Alsancak+Nevvar+Salih+%C4%B0%C5%9Fg%C3%B6ren+Devlet+Hastanesi/@44.8869346,-25.0364219,3z/data=!4m6!3m5!1s0x14bbd85958184dd7:0xd461326cb2dc8ae5!8m2!3d38.4343139!4d27.1430765!16s%2Fg%2F1td0jq68?entry=ttu&g_ep=EgoyMDI2MDQxMy4wIKXMDSoASAFQAw%3D%3D',
    'Dokuz Eylul Hospital': 'https://www.google.com/maps/place/%C4%B0nciralt%C4%B1,+Dokuz+Eyl%C3%BCl+%C3%9Cnv.+Hst.,+35330+Bal%C3%A7ova%2F%C4%B0zmir/@38.3947432,27.0220664,15z/data=!3m1!4b1!4m6!3m5!1s0x14bbdcf5f4c482e5:0x9714797844847353!8m2!3d38.3947268!4d27.0323447!16s%2Fg%2F11byl25n2x?entry=ttu&g_ep=EgoyMDI2MDQxMy4wIKXMDSoASAFQAw%3D%3D',
    'Cigli Training and Research State Hospital': 'https://www.google.com/maps/place/%C3%87i%C4%9Fli+E%C4%9Fitim+Ara%C5%9Ft%C4%B1rma+Devlet+Hastanesi/@38.5010481,27.0488833,17z/data=!4m15!1m8!3m7!1s0x14bbd09a6a8bcb45:0xd26ccc739379d84b!2zS8O8w6fDvGsgw4dpxJ9saSwgODc4MC8xMS4gU2suIE5vOjM1LCAzNTYxMCBBb3NiL8OHacSfbGkvxLB6bWly!3b1!8m2!3d38.5010481!4d27.0488833!16s%2Fg%2F11q2nlklxc!3m5!1s0x14bbd09a31c767c1:0x4cc049ecf86c6593!8m2!3d38.4998565!4d27.0494967!16s%2Fg%2F11g8wh0kj9?entry=ttu&g_ep=EgoyMDI2MDQxMy4wIKXMDSoASAFQAw%3D%3D'
}
OSRM_TABLE_BASE_URL = "https://router.project-osrm.org/table/v1/driving/"

distance_matrix = {
    'Bornova': [2.0, 10.0, 12.0, 8.0, 25.0, 15.0],
    'Karsiyaka': [12.0, 15.0, 14.0, 10.0, 28.0, 8.0],
    'Buca': [15.0, 8.0, 10.0, 18.0, 20.0, 25.0],
    'Konak': [12.0, 5.0, 2.0, 15.0, 18.0, 22.0],
    'Cigli': [18.0, 20.0, 22.0, 16.0, 35.0, 3.0],
    'Balcova': [25.0, 18.0, 16.0, 28.0, 5.0, 30.0]
}

doctor_data = {
    'Doctor_Name': [
        'Prof. Dr. Ahmet Yılmaz', 'Assoc. Prof. Dr. Ayşe Demir', 'Spec. Dr. Mehmet Kaya', 
        'Prof. Dr. Fatma Şahin', 'Spec. Dr. Ali Can', 'Assoc. Prof. Dr. Zeynep Çelik',
        'Prof. Dr. Hasan Yıldız', 'Spec. Dr. Elif Arslan', 'Assoc. Prof. Dr. Burak Tekin',
        'Prof. Dr. Selin Vural', 'Spec. Dr. Cemal Öztürk', 'Assoc. Prof. Dr. Derya Bulut',
        'Spec. Dr. Kemal Taran', 'Prof. Dr. Leyla Keskin', 'Spec. Dr. Murat Sönmez'
    ],
    'Specialty': [
        'Endocrinology', 'Endocrinology', 'Internal Medicine', 'Endocrinology', 'Internal Medicine', 'Endocrinology',
        'Endocrinology', 'Endocrinology', 'Internal Medicine', 'Endocrinology', 'General Surgery', 'Endocrinology',
        'Internal Medicine', 'Endocrinology', 'Internal Medicine'
    ],
    'Hospital': [
        'Ege University Hospital', 'Dokuz Eylul Hospital', 'Tepecik Training and Research Hospital',
        'Izmir City Hospital', 'Alsancak Nevvar Salih Isgoren State Hospital', 'Cigli Training and Research State Hospital',
        'Tepecik Training and Research Hospital', 'Ege University Hospital', 'Izmir City Hospital',
        'Dokuz Eylul Hospital', 'Alsancak Nevvar Salih Isgoren State Hospital', 'Cigli Training and Research State Hospital',
        'Ege University Hospital', 'Alsancak Nevvar Salih Isgoren State Hospital', 'Dokuz Eylul Hospital'
    ],
    'Experience_Years': [25, 15, 8, 30, 5, 18, 28, 10, 16, 32, 12, 14, 7, 26, 9],
    'Patient_Satisfaction': [4.8, 4.6, 3.9, 4.9, 4.1, 4.7, 4.5, 4.3, 4.4, 4.9, 3.8, 4.6, 4.0, 4.7, 4.2]
}
df_doctors = pd.DataFrame(doctor_data)

def score_title(name):
    if "Prof." in name: return 100
    elif "Assoc. Prof." in name: return 80
    elif "Spec." in name: return 60
    else: return 40

def parse_num(val):
    try:
        if val is None or str(val).strip() == "": return None
        return float(str(val).replace(',', '.'))
    except ValueError:
        return None

def haversine_km(lat1, lon1, lat2, lon2):
    earth_radius_km = 6371.0
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
    )
    return 2 * earth_radius_km * math.asin(math.sqrt(a))


def build_hospital_map_url(hospital_name):
    return hospital_map_urls.get(hospital_name, "https://www.google.com/maps")

def get_osrm_route_metrics(user_lat, user_lng, hospital_coords):
    hospital_names = list(hospital_coords.keys())
    points = [(user_lng, user_lat)] + [(coords[1], coords[0]) for coords in hospital_coords.values()]
    coordinates = ";".join(f"{lon},{lat}" for lon, lat in points)
    query = urllib.parse.urlencode({
        "sources": "0",
        "annotations": "distance,duration"
    })
    url = f"{OSRM_TABLE_BASE_URL}{coordinates}?{query}"

    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))

        distances = payload.get("distances", [[]])[0][1:]
        durations = payload.get("durations", [[]])[0][1:]
        metrics = {}

        for i, hospital_name in enumerate(hospital_names):
            distance_m = distances[i] if i < len(distances) else None
            duration_s = durations[i] if i < len(durations) else None
            if distance_m is None:
                continue
            metrics[hospital_name] = {
                "distance_km": float(distance_m) / 1000.0,
                "eta_min": (float(duration_s) / 60.0) if duration_s is not None else None
            }
        return metrics
    except Exception:
        return {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/model-info', methods=['GET'])
def model_info():
    return jsonify({
        "model_path": MODEL_PATH,
        "metadata_path": MODEL_METADATA_PATH,
        "model_exists": os.path.exists(MODEL_PATH),
        "metadata": model_metadata
    })

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid request payload."}), 400
    
    age = parse_num(data.get('age'))
    tsh = parse_num(data.get('tsh'))
    t3 = parse_num(data.get('t3'))
    tt4 = parse_num(data.get('tt4'))
    t4u = parse_num(data.get('t4u'))
    fti = parse_num(data.get('fti'))
    user_lat = parse_num(data.get('lat'))
    user_lng = parse_num(data.get('lng'))
    requested_district = data.get('district', 'Bornova')
    district = requested_district if requested_district in distance_matrix else 'Bornova'
    use_live_location = user_lat is not None and user_lng is not None

    if age is not None and (age < 0 or age > 120):
        return jsonify({"error": "Age must be between 0 and 120."}), 400

    if (user_lat is None) != (user_lng is None):
        return jsonify({"error": "Both latitude and longitude are required for live location."}), 400
    if user_lat is not None and (user_lat < -90 or user_lat > 90):
        return jsonify({"error": "Latitude must be between -90 and 90."}), 400
    if user_lng is not None and (user_lng < -180 or user_lng > 180):
        return jsonify({"error": "Longitude must be between -180 and 180."}), 400
        
    hormones_to_check = [tsh, t3, tt4, t4u, fti]
    if any(v is not None and v < 0 for v in hormones_to_check):
        return jsonify({"error": "Laboratory values cannot be negative."}), 400

    if tsh is not None and tsh > 556.5:
        return jsonify({"error": "TSH value exceeds the dataset threshold (Max 556.5)."}), 400
    if fti is not None and fti > 414.8:
        return jsonify({"error": "FTI value exceeds the dataset threshold (Max 414.8)."}), 400
    if t3 is not None and t3 > 18.9:
        return jsonify({"error": "Total T3 value exceeds the dataset threshold (Max 18.9)."}), 400
    if tt4 is not None and tt4 > 451.5:
        return jsonify({"error": "Total T4 value exceeds the dataset threshold (Max 451.5)."}), 400
    if t4u is not None and t4u > 2.42:
        return jsonify({"error": "T4 Uptake value exceeds the dataset threshold (Max 2.42)."}), 400

    if all(v is None for v in hormones_to_check):
        diagnosis = "Unknown"
        confidence = 0.0
    else:
        input_data = {col: X_train[col].mode()[0] for col in X_train.columns}
        
        if tsh is not None and 'TSH measured' in input_data: input_data['TSH measured'] = 1
        if fti is not None and 'FTI measured' in input_data: input_data['FTI measured'] = 1
        if t3 is not None and 'T3 measured' in input_data: input_data['T3 measured'] = 1
        if tt4 is not None and 'TT4 measured' in input_data: input_data['TT4 measured'] = 1
        if t4u is not None and 'T4U measured' in input_data: input_data['T4U measured'] = 1
        
        input_data['age'] = age if age is not None else X_train['age'].median()
        input_data['sex'] = 1 if data.get('gender') == "Male" else 0
        
        input_data['TSH'] = tsh if tsh is not None else X_train['TSH'].median()
        input_data['T3'] = t3 if t3 is not None else X_train['T3'].median()
        input_data['TT4'] = tt4 if tt4 is not None else X_train['TT4'].median()
        input_data['T4U'] = t4u if t4u is not None else X_train['T4U'].median()
        input_data['FTI'] = fti if fti is not None else X_train['FTI'].median()

        df_input = pd.DataFrame([input_data])[X_train.columns]
        
        probs = catboost_model.predict_proba(df_input)[0]
        confidence = max(probs) * 100
        pred_code = int(catboost_model.predict(df_input).flatten()[0])
        
        conditions = {0: "Hyperthyroidism", 1: "Hypothyroidism", 2: "Healthy"}
        diagnosis = conditions.get(pred_code, "Unknown")

        if tsh is not None:
            if tsh >= 4.5:
                diagnosis = "Hypothyroidism"
                confidence = 98.9
            elif tsh <= 0.4:
                diagnosis = "Hyperthyroidism"
                confidence = 98.9
                
        if fti is not None:
            if fti <= 65 and diagnosis == "Healthy":
                diagnosis = "Hypothyroidism"
                confidence = 97.5
            elif fti >= 145 and diagnosis == "Healthy":
                diagnosis = "Hyperthyroidism"
                confidence = 97.5

    top_doctors = []
    distance_source = "district"
    
    if diagnosis != "Healthy":
        suitable_doctors = df_doctors[df_doctors['Specialty'].isin(['Endocrinology', 'Internal Medicine'])].copy()
        if use_live_location:
            route_metrics = get_osrm_route_metrics(user_lat, user_lng, hospital_coordinates)
            if route_metrics:
                distance_source = "live_route"
                hospital_distances = {h: route_metrics[h]["distance_km"] for h in route_metrics}
                hospital_eta = {h: route_metrics[h]["eta_min"] for h in route_metrics}
            else:
                distance_source = "live_location_fallback"
                hospital_distances = {
                    hospital: haversine_km(user_lat, user_lng, coords[0], coords[1])
                    for hospital, coords in hospital_coordinates.items()
                }
                hospital_eta = {}
        else:
            hospital_distances = dict(zip(hospitals, distance_matrix[district]))
            hospital_eta = {}

        suitable_doctors['Distance'] = suitable_doctors['Hospital'].map(hospital_distances)
        suitable_doctors['Eta_Min'] = suitable_doctors['Hospital'].map(hospital_eta)
        suitable_doctors['Eta_Min'] = suitable_doctors['Eta_Min'].round(0)
        suitable_doctors['Title_Score'] = suitable_doctors['Doctor_Name'].apply(score_title)
        suitable_doctors['Map_Url'] = suitable_doctors['Hospital'].map(build_hospital_map_url)
        suitable_doctors = suitable_doctors.dropna(subset=['Distance'])
        
        suitable_doctors['Score'] = (
            (suitable_doctors['Experience_Years'] * 0.2) + 
            ((np.clip(50 - suitable_doctors['Distance'], 0, 50)) * 0.3) + 
            (suitable_doctors['Patient_Satisfaction'] * 10 * 0.25) + 
            (suitable_doctors['Title_Score'] * 0.25)
        )
        suitable_doctors['Distance'] = suitable_doctors['Distance'].round(1)
        top_doctors = suitable_doctors.sort_values(by='Score', ascending=False).head(5).to_dict(orient='records')
        
    return jsonify({
        'diagnosis': diagnosis,
        'confidence': round(confidence, 1),
        'tsh_val': round(tsh, 2) if tsh is not None else round(X_train['TSH'].median(), 2),
        'fti_val': round(fti, 1) if fti is not None else round(X_train['FTI'].median(), 1),
        'distance_source': distance_source,
        'doctors': top_doctors,
        'disclaimer': DISCLAIMER_TEXT
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", "7860"))
    app.run(host='0.0.0.0', port=port)