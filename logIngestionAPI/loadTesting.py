import requests
import random
import json
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Define the endpoint URL
endpoint_url = 'http://0.0.0.0:3000/logIngest'

# Arrays with expanded values for more combinations
levels = ['info', 'warning', 'error', 'debug']
messages = ['Failed to connect to DB', 'Service unavailable', 'Invalid input received', 'Timeout error']
resource_ids = ['server-1234', 'server-5678', 'server-91011', 'server-121314']
trace_ids = ['abc-xyz-123', 'def-uvw-456', 'ghi-rst-789', 'jkl-mno-101112']
span_ids = ['span-456', 'span-789', 'span-101112', 'span-131415']
commits = ['5e5342f', '6a78b9c', '1d2e3f4', '7g8h9i0j']
parent_resource_ids = ['server-0987', 'server-6543', 'server-3210', 'server-161718']

# Function to generate a random log record
def generate_log_record():
    log_record = {
        "level": random.choice(levels),
        "message": random.choice(messages),
        "resourceId": random.choice(resource_ids),
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "traceId": random.choice(trace_ids),
        "spanId": random.choice(span_ids),
        "commit": random.choice(commits),
        "metadata": {
            "parentResourceId": random.choice(parent_resource_ids)
        }
    }
    return log_record

# Function to send log record to endpoint
def send_log_record(log_record):
    try:
        response = requests.post(endpoint_url, json=log_record)
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        print("Error:", str(e))
        return False

# Main function to generate and send log records concurrently
def main(num_records, num_threads):
    start_time = time.time()
    successful_ingestions = 0
    failed_ingestions = 0
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(send_log_record, generate_log_record()) for _ in range(num_records)]
        for future in futures:
            if future.result():
                successful_ingestions += 1
            else:
                failed_ingestions += 1
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Successful ingestions: {successful_ingestions}")
    print(f"Failed ingestions: {failed_ingestions}")
    print(f"Total time elapsed: {total_time} seconds")

if __name__ == "__main__":
    num_records = 10000  # Change this number as per the desired load
    num_threads = 10  # Adjust the number of threads for concurrency
    main(num_records, num_threads)
