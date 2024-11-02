import pandas as pd
import numpy as np
from sklearn.ensemble import StackingClassifier, GradientBoostingClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from imblearn.over_sampling import SMOTE
import joblib
from encoder import encode_features, encode_labels
from scaler import scale_features

# Load and preprocess dataset
dataset = pd.read_csv('maternal_health_risk.csv')

# Feature engineering
dataset['BPRatio'] = dataset['SystolicBP'] / dataset['DiastolicBP']
dataset['PulseRate'] = dataset['HeartRate'] / dataset['Age']
dataset['MaxHeartRate'] = 220 - dataset['Age']
dataset['HeartRateRatio'] = dataset['HeartRate'] / dataset['MaxHeartRate']
dataset['Fever'] = dataset['BodyTemp'].apply(lambda x: 1 if x - 98.6 > 0 else 0)
dataset['Hypertension'] = ((dataset['SystolicBP'] >= 130) | (dataset['DiastolicBP'] >= 80)).astype(int)
dataset['Prediabetes'] = dataset['BS'].apply(lambda x: 1 if 5.6 <= x <= 6.9 else 0)
dataset['Diabetes'] = dataset['BS'].apply(lambda x: 1 if x >= 7 else 0)
dataset['age_bpratio_interaction'] = dataset['Age'] * dataset['BPRatio']
dataset['age_bs_interaction'] = dataset['Age'] * dataset['BS']

bins = [0, 19, 29, 39, 49, 59, 69, 120]
labels = ['0-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70+']
dataset['AgeGroup'] = pd.cut(dataset['Age'], bins=bins, labels=labels, right=False)

order = ['AgeGroup', 'BPRatio', 'HeartRateRatio', 'PulseRate', 'Fever', 'Hypertension', 'BS', 'Prediabetes', 'Diabetes',
         'age_bpratio_interaction', 'age_bs_interaction', 'RiskLevel']
dataset = dataset[order]

x = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

x = encode_features(x)
y, label_encoder = encode_labels(y)

# SMOTE for balancing
smote = SMOTE(random_state=42)
x, y = smote.fit_resample(x, y)

# Train-test split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Scale features
x_train, x_test, scaler = scale_features(x_train, x_test)

# Save scaler for later use
joblib.dump(scaler, 'scaler.joblib')

# Define and train model
et = ExtraTreesClassifier(n_estimators=100, random_state=42)
gb = GradientBoostingClassifier(n_estimators=100, random_state=42)
svc = SVC(probability=True, random_state=42)

classifier = StackingClassifier(
    estimators=[('et', et), ('gb', gb), ('svc', svc)],
    final_estimator=LogisticRegression(),
    cv=5,
)
classifier.fit(x_train, y_train)

# Save model
joblib.dump(classifier, 'model.joblib')

# Evaluation
y_pred = classifier.predict(x_test)
print(classification_report(y_test, y_pred))
print('Confusion Matrix:\n', confusion_matrix(y_test, y_pred))
print('Accuracy Score:', accuracy_score(y_test, y_pred))

