import pandas as pd
from sqlalchemy import select
from heimdall.database import engine, SystemMetric
import joblib 
import os

MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'heimdall', 'models', 'local_model.pkl')

def load_trained_model():
    """Loads a trained model from a file."""
    if os.path.exists(MODEL_PATH):
        try:
            return joblib.load(MODEL_PATH)
        except Exception as e:
            print(f"Error loading model from {MODEL_PATH}: {e}")
            return None
    return None

def load_metrics_to_df():
    """
    Loads all system metrics from the database into a pandas DataFrame.
    """
    with engine.connect() as connection:
        query = select(SystemMetric).order_by(SystemMetric.timestamp)
        df = pd.read_sql(query, connection, index_col='id', parse_dates=['timestamp'])
    return df

def generate_simple_report(df: pd.DataFrame):
    """
    Generates a text-based report from the collected metrics,
    including anomaly detection if a model is available.
    """
    if df.empty:
        return "No metrics collected yet to generate a report."

    report = "--- Heimdall System Report ---\n"
    report += f"Total metrics collected: {len(df)}\n"
    report += f"Time range: {df['timestamp'].min()} to {df['timestamp'].max()}\n"
    report += "\n--- CPU Usage ---\n"
    report += f"Average: {df['cpu_percent'].mean():.2f}%\n"
    report += f"Max: {df['cpu_percent'].max():.2f}%\n"
    report += f"Min: {df['cpu_percent'].min():.2f}%\n"
    report += "\n--- Memory Usage ---\n"
    report += f"Average: {df['memory_percent'].mean():.2f}%\n"
    report += f"Max: {df['memory_percent'].max():.2f}%\n"
    report += f"Min: {df['memory_percent'].min():.2f}%\n"
    report += "\n--- Process Count ---\n"
    report += f"Average: {df['process_count'].mean():.0f}\n"
    report += f"Max: {df['process_count'].max():.0f}\n"
    report += f"Min: {df['process_count'].min():.0f}\n"
    report += "\n--- Active Network Connections ---\n"
    report += f"Average: {df['active_network_connections'].mean():.0f}\n"
    report += f"Max: {df['active_network_connections'].max():.0f}\n"
    report += f"Min: {df['active_network_connections'].min():.0f}\n"

    # Anomaly Detection section (new)
    model = load_trained_model()
    if model:
        report += "\n--- Anomaly Detection ---\n"
        # Features used for training (must match train_model.py)
        features = ['cpu_percent', 'memory_percent', 'active_network_connections']
        if not all(f in df.columns for f in features):
            report += "  Warning: Not all features for anomaly detection present in data.\n"
        else:
            X = df[features]
            # Predict anomalies: -1 for outliers, 1 for inliers
            df['anomaly'] = model.predict(X)
            
            anomalies = df[df['anomaly'] == -1]
            if not anomalies.empty:
                report += f"  {len(anomalies)} potential anomalies detected.\n"
                report += "  Timestamp of first 5 anomalies:\n"
                for i, row in anomalies.head(5).iterrows():
                    report += (f"    - {row['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}: "
                               f"CPU={row['cpu_percent']:.1f}%, Mem={row['memory_percent']:.1f}%, "
                               f"Net={row['active_network_connections']:.0f}\n")
                if len(anomalies) > 5:
                    report += "    (and more...)\n"
            else:
                report += "  No significant anomalies detected in this period.\n"
    else:
        report += "\n--- Anomaly Detection ---\n"
        report += "  No anomaly detection model found. Run 'scripts/train_model.py' first.\n"

    report += "---------------------------\n"
    return report

if __name__ == '__main__':
    # Example of how to use this module
    df_metrics = load_metrics_to_df()
    print(df_metrics.head())
    print(generate_simple_report(df_metrics))
