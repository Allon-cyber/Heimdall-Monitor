import psutil
import time
import os
import sys

# Add the parent directory to the system path to allow importing sibling modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from heimdall.database import save_metric, init_db

def collect_all_metrics():
    """
    Collects system-wide metrics (CPU, Memory, Process Count)
    and saves them to the database.
    """
    cpu_percent = psutil.cpu_percent(interval=1)  # Blocking, calculates CPU usage over 1 second
    memory_percent = psutil.virtual_memory().percent
    process_count = len(psutil.pids())
    active_network_connections = len(psutil.net_connections())

    metric = save_metric(cpu_percent, memory_percent, process_count, active_network_connections)
    print(f"Collected and saved: {metric}")
    return metric

def start_collector_daemon(interval=60):
    """
    Starts the metric collector as a daemon, running in a loop.
    """
    print(f"Heimdall collector started. Collecting metrics every {interval} seconds.")
    init_db() # Ensure DB is initialized when collector starts
    while True:
        try:
            collect_all_metrics()
        except Exception as e:
            print(f"Error during metric collection: {e}")
        time.sleep(interval)

if __name__ == "__main__":
    # Ensure the database is initialized
    init_db()
    
    # For testing, collect a few metrics and then stop
    print("Collecting 3 metrics for testing purposes...")
    for _ in range(3):
        collect_all_metrics()
        time.sleep(2) # Shorter interval for quick test
    print("Test collection complete.")

    # To run as a continuous daemon, uncomment the line below:
    # start_collector_daemon(interval=10) # Example: collect every 10 seconds
