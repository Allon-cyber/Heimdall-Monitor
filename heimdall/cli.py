import click
import os
import sys
import subprocess
from dotenv import load_dotenv

# Add the parent directory to the system path to allow importing sibling modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from heimdall.collector import start_collector_daemon
from heimdall.analysis import load_metrics_to_df, generate_simple_report
from heimdall.ai_analyzer import get_gemini_api_key # Added import

@click.group()
def cli():
    """Heimdall - Intelligent System Monitor"""
    pass

@cli.command()
def hello():
    """Says hello."""
    click.echo("Hello from Heimdall!")

@cli.command()
@click.option('--interval', default=60, help='Interval in seconds for metric collection.')
def start_collector(interval):
    """Starts the data collector daemon."""
    click.echo(f"Starting Heimdall data collector with interval: {interval} seconds...")
    start_collector_daemon(interval=interval)

@cli.command()
def report():
    """Generates a system performance report."""
    click.echo("Generating system performance report...")
    df = load_metrics_to_df()
    report_text = generate_simple_report(df)
    click.echo(report_text)

@cli.command()
def train():
    """Trains the anomaly detection model."""
    script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts', 'train_model.py')
    click.echo(f"Starting model training using {script_path}...")
    try:
        # Use sys.executable to ensure the script runs with the same Python interpreter (from venv)
        result = subprocess.run([sys.executable, script_path], check=True, capture_output=True, text=True)
        click.echo(result.stdout)
        if result.stderr:
            click.echo("Error during training:")
            click.echo(result.stderr)
    except subprocess.CalledProcessError as e:
        click.echo(f"Model training failed with exit code {e.returncode}:")
        click.echo(e.stdout)
        click.echo(e.stderr)
    except FileNotFoundError:
        click.echo(f"Error: Training script not found at {script_path}")
    click.echo("Model training command finished.")

@cli.command()
def configure():
    """Configures Heimdall settings, including API keys."""
    click.echo("--- Heimdall Configuration ---")
    
    # Configure Gemini API Key
    api_key_prompt = "Enter your Gemini API Key (leave empty to skip): "
    current_key = get_gemini_api_key()
    if current_key:
        api_key_prompt = f"Enter your Gemini API Key (current: {'*' * len(current_key)}, leave empty to keep current): "
    
    gemini_api_key = click.prompt(api_key_prompt, default=current_key or '', hide_input=True)
    
    env_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')

    env_content = []
    if os.path.exists(env_file_path):
        with open(env_file_path, 'r') as f:
            env_content = f.readlines()

    key_found = False
    with open(env_file_path, 'w') as f:
        for line in env_content:
            if line.strip().startswith("GEMINI_API_KEY="):
                if gemini_api_key:
                    f.write(f"GEMINI_API_KEY=\"{gemini_api_key}\"\n")
                    click.echo("Gemini API Key updated.")
                else:
                    click.echo("Gemini API Key kept as current.")
                key_found = True
            else:
                f.write(line)
        if not key_found and gemini_api_key:
            f.write(f"GEMINI_API_KEY=\"{gemini_api_key}\"\n")
            click.echo("Gemini API Key added.")
        elif not key_found and not gemini_api_key:
            click.echo("No Gemini API Key provided and none was set.")
    
    click.echo("Configuration complete. Remember to restart any running Heimdall processes for changes to take effect.")

if __name__ == '__main__':
    cli()
