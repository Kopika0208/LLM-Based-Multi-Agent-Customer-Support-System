import logging
import os
import csv
from datetime import datetime

# Ensure logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# CSV log file
CSV_FILE = os.path.join(LOG_DIR, "chat_logs.csv")

# Setup Python logging (console & file)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "app.log")),
        logging.StreamHandler()
    ]
)

def log_to_csv(user_query, agent_response, agent_name):
    """
    Logs each interaction in CSV: timestamp, user query, agent response, agent
    """
    # If file does not exist, write header
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "agent", "user_query", "agent_response"])

    # Append log
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), agent_name, user_query, agent_response])

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

def log_debug(message):
    logging.debug(message)
