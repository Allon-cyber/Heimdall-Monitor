import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

def get_gemini_api_key():
    """Retrieves the Gemini API key from environment variables."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not found in environment variables or .env file.")
        print("Please configure it using 'heimdall configure' command.")
    return api_key

def explain_anomaly_with_gemini(metrics_df, anomaly_info, user_question):
    """
    Placeholder function to interact with the Gemini API to explain anomalies.
    Will be fully implemented later.
    """
    api_key = get_gemini_api_key()
    if not api_key:
        return "Cannot explain anomaly: Gemini API key not configured."

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    # Placeholder: construct a simple prompt for now
    prompt = (
        f"The user asked: '{user_question}'\n"
        f"System metrics for the relevant period:\n{metrics_df.to_string()}\n"
        f"Anomaly detected: {anomaly_info}\n\n"
        "Based on this data, explain in simple terms why the server might have been slow, "
        "focusing on the most relevant factors from the metrics and anomaly."
    )

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error communicating with Gemini API: {e}"

if __name__ == "__main__":
    # Example usage (requires GEMINI_API_KEY to be set and some dummy data)
    print("This module is intended for integration. Run 'heimdall configure' first.")
    key = get_gemini_api_key()
    if key:
        print("Gemini API key loaded. (Not making an actual call in __main__ block).")
