# scaler.py

from sklearn.preprocessing import StandardScaler
import joblib

def scale_features(x_train, x_test):
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)
    return x_train_scaled, x_test_scaled, scaler

# Load scaler for later use in Flask app
def load_scaler():
    return joblib.load('scaler.joblib')

