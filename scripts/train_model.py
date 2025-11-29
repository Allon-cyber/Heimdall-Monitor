import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import os
import sys

# Add the parent directory to the system path to allow importing sibling modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from heimdall.analysis import load_metrics_to_df

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'heimdall', 'models', 'local_model.pkl')

def train_anomaly_model(df: pd.DataFrame):
    """
    Trains an Isolation Forest model for anomaly detection on system metrics.
    """
    if df.empty:
        print("Error: No data available for training the model.")
        return None

    # Features for anomaly detection
    # Exclude 'timestamp' and 'process_count' for now as they might not scale well
    # 'process_count' can be tricky, as its absolute value might vary.
    # We might consider deriving features from process_count (e.g., changes over time)
    # For a start, focus on continuous resource usage.
    features = ['cpu_percent', 'memory_percent', 'active_network_connections']
    
    X = df[features]

    # Initialize and train the Isolation Forest model
    # contamination is the expected proportion of outliers in the data set.
    # We'll set a default, but this can be tuned.
    model = IsolationForest(random_state=42, contamination=0.01) 
    model.fit(X)
    
    return model

def save_model(model, path=MODEL_PATH):
    """Saves the trained model to a file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    print(f"Model saved to {path}")

def load_model(path=MODEL_PATH):
    """Loads a trained model from a file."""
    if os.path.exists(path):
        return joblib.load(path)
    return None

if __name__ == '__main__':
    print("Starting model training...")
    df_metrics = load_metrics_to_df()
    
    if df_metrics.empty:
        print("No metrics collected yet. Please run the collector for some time before training.")
        sys.exit(1)

    print(f"Loaded {len(df_metrics)} metrics for training.")
    model = train_anomaly_model(df_metrics)
    
    if model:
        save_model(model)
        print("Model training complete.")
    else:
        print("Model training failed.")
        sys.exit(1)
