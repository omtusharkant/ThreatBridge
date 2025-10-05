import requests
import json
import time

# --- Configuration ---
# Replace with the actual URL of your Django server
SERVER_URL = 'http://127.0.0.1:8000/api/log_collector/' 
# Replace with the API key you set in your Django settings.py
API_KEY = 'YOUR_SECRET_API_KEY' 

def send_logs(log_data):
    """
    Sends a batch of log data to the Django server.
    """
    headers = {
        'Content-Type': 'application/json',
        'X-API-KEY': API_KEY,
    }
    payload = {
        'logs': log_data
    }

    try:
        response = requests.post(SERVER_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        print(f"Successfully sent logs. Server responded with: {response.json()}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred with the request: {req_err}")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")

if __name__ == "__main__":
    # --- Example Usage ---
    # This is a simple example. In a real-world scenario, you would
    # read logs from a file, a systemd journal, or another source.
    
    print("Log sender script started.")
    
    # Example: Send a new log message every 10 seconds
    log_counter = 1
    while True:
        # Create a sample log entry in the new structured format
        log_entry = {
            "message": f"New user login from IP 192.168.1.{log_counter}",
            "source": "auth_service",
            "level": "INFO"
        }
        
        print(f"Sending log: {log_entry}")
        
        # The API is designed to receive a list of logs
        send_logs([log_entry])
        
        log_counter += 1
        time.sleep(10)
