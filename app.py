from flask import Flask, request, jsonify
import joblib
import numpy as np
import pandas as pd

# Load the trained model and preprocessing objects
model = joblib.load('model.joblib')
scaler = joblib.load('scaler.joblib')
label_encoder = joblib.load('label_encoder.joblib')
feature_encoder = joblib.load('encoder.joblib')

app = Flask(__name__)

# Define age bins and labels
age_bins = [0, 19, 29, 39, 49, 59, 69, 120]
age_labels = ['0-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70+']

def calculate_features(data):
    age = data['Age']
    systolic_bp = data['SystolicBP']
    diastolic_bp = data['DiastolicBP']
    bs = data['BS']
    body_temp = data['BodyTemp']
    heart_rate = data['HeartRate']

    # Feature Engineering
    age_group = pd.cut([age], bins=age_bins, labels=age_labels, right=False)[0]
    bp_ratio = systolic_bp / diastolic_bp if diastolic_bp != 0 else 0
    heart_rate_ratio = heart_rate / (220 - age) if age != 0 else 0
    pulse_rate = heart_rate
    fever = 1 if body_temp > 98.6 else 0
    hypertension = 1 if systolic_bp >= 130 or diastolic_bp >= 80 else 0
    prediabetes = 1 if 5.6 <= bs <= 6.9 else 0
    diabetes = 1 if bs >= 7 else 0
    age_bpratio_interaction = age * bp_ratio
    age_bs_interaction = age * bs

    features = {
        'AgeGroup': age_group,
        'BPRatio': bp_ratio,
        'HeartRateRatio': heart_rate_ratio,
        'PulseRate': pulse_rate,
        'Fever': fever,
        'Hypertension': hypertension,
        'BS': bs,
        'Prediabetes': prediabetes,
        'Diabetes': diabetes,
        'age_bpratio_interaction': age_bpratio_interaction,
        'age_bs_interaction': age_bs_interaction
    }
    return features

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No input data provided'}), 400

    required_fields = ['Age', 'SystolicBP', 'DiastolicBP', 'HeartRate', 'BodyTemp', 'BS']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    # Transform input data
    features = calculate_features(data)

    # Prepare input array (adjust for required feature order)
    input_data = np.array([[
        features['AgeGroup'],
        features['BPRatio'],
        features['HeartRateRatio'],
        features['PulseRate'],
        features['Fever'],
        features['Hypertension'],
        features['BS'],
        features['Prediabetes'],
        features['Diabetes'],
        features['age_bpratio_interaction'],
        features['age_bs_interaction']
    ]])

    # Apply feature encoding
    encoded_features = feature_encoder.transform(input_data)

    # Scale input
    scaled_features = scaler.transform(encoded_features)

    # Predict and decode the result
    prediction = model.predict(scaled_features)
    prediction_label = label_encoder.inverse_transform(prediction)

    return jsonify({'prediction': prediction_label[0]})

if __name__ == '__main__':
    app.run(debug=True)
