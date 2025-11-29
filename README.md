# Heimdall - Intelligent System Monitor

Heimdall is an intelligent system monitor designed to collect and analyze resource usage data (CPU, RAM, Disk I/O, Network) and provide insightful answers to performance-related questions about your computer.

A core feature of Heimdall is its "self-learning" capability. This means that after an initial data collection phase, it can train a personalized Machine Learning model tailored to your specific system's "fingerprint." This ensures that the analysis is precise and optimized for the unique behavior of each machine.

## Features

-   Monitoring of CPU, RAM, Disk I/O, and Network usage.
-   Historical data collection into a lightweight SQLite database.
-   Anomaly detection and performance issue identification using a trained Machine Learning model.
-   Command-Line Interface (CLI) for querying and receiving intelligent reports.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/Allon-cyber/Heimdall-Monitor
    cd Heimdall
    ```
2.  Create and activate a Python virtual environment (recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## First Run and Model Training

Upon first launch, Heimdall will begin collecting data about your system in the background. After sufficient data has been gathered (we recommend a minimum of 24 hours), you can train your personalized analytical model.

1.  Start Heimdall (this will initiate data collection):
    ```bash
    python -m heimdall.cli
    ```

2.  After data collection, train the model:
    ```bash
    python scripts/train_model.py
    ```

3.  Now you can ask questions and receive intelligent reports!
    ```bash
    python -m heimdall.cli report --time '1 hour ago'
    ```

## Usage

```bash
python -m heimdall.cli --help
```

## Development

We encourage contributions to Heimdall! Feel free to add new data collection modules, improve analysis algorithms, or create new interfaces. Check the files in the `heimdall/` directory.
