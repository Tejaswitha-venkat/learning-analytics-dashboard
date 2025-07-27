from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class RiskPredictor:
    def __init__(self):
        self.model = RandomForestClassifier()
        self.scaler = StandardScaler()
    
    def predict(self, features):
        scaled_features = self.scaler.transform(features)
        return self.model.predict_proba(scaled_features)