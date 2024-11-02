# encoder.py

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import numpy as np
import joblib

# Encoder setup function for categorical features in x
def encode_features(x):
    # Assume column 0 (AgeGroup) needs encoding as in your original code
    column_transformer = ColumnTransformer(
        transformers=[('encoder', OneHotEncoder(), [0])],
        remainder="passthrough"
    )
    x_encoded = np.array(column_transformer.fit_transform(x))
    # Save the encoder for reuse in the Flask app
    joblib.dump(column_transformer, 'encoder.joblib')
    return x_encoded

# Label encoding for target variable y
def encode_labels(y):
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    # Save the label encoder for reuse in the Flask app
    joblib.dump(label_encoder, 'label_encoder.joblib')
    return y_encoded, label_encoder

# Load encoders for later use in Flask app
def load_encoder():
    return joblib.load('encoder.joblib')

def load_label_encoder():
    return joblib.load('label_encoder.joblib')

