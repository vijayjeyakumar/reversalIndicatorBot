from datetime import datetime, time
import functionalityToCheckOneTwentyReversal as oneTwenty
import time as tm
import threading

# Hardcoded values
access_token = "eyJ0eXAiOiJKV1QiLCJrZXlfaWQiOiJza192MS4wIiwiYWxnIjoiSFMyNTYifQ.eyJzdWIiOiI0MzU2NzEiLCJqdGkiOiI2NzZlMjRhZmE1MjBlYjBiYTc5MGFkOWQiLCJpc011bHRpQ2xpZW50IjpmYWxzZSwiaWF0IjoxNzM1MjcxNTk5LCJpc3MiOiJ1ZGFwaS1nYXRld2F5LXNlcnZpY2UiLCJleHAiOjE3MzUzMzY4MDB9.JtHXNHZ9ygfUjXmWYC5zwQHkpCnxFc9-fBCZYVu5b3M"
base_url = "https://api.upstox.com"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}
# make instrument key as list in future
instrument_keys = [
    "NSE_INDEX|Nifty Auto", "NSE_INDEX|Nifty Media", "NSE_INDEX|Nifty Midcap 50", "NSE_INDEX|Nifty Realty",
    "NSE_INDEX|Nifty Bank",
    "NSE_INDEX|Nifty IT", "NSE_INDEX|Nifty 50", "NSE_INDEX|Nifty Fin Service", "NSE_INDEX|Nifty FMCG",
    "NSE_INDEX|Nifty Pharma",
    "NSE_INDEX|Nifty PSU Bank", "NSE_INDEX|Nifty Media", "NSE_INDEX|Nifty Infra", "NSE_INDEX|Nifty Next 50",
    "NSE_INDEX|NIFTY SMLCAP 50", "NSE_INDEX|Nifty Pvt Bank", "NSE_INDEX|NIFTY OIL AND GAS"
]

timeFrames = [

    {"timeFrame": "09:30:00", "displayTime": "9:30 AM"},
    {"timeFrame": "09:35:00", "displayTime": "9:35 AM"},
    {"timeFrame": "09:40:00", "displayTime": "9:40 AM"},

    {"timeFrame": "09:45:00", "displayTime": "9:45 AM"},
    {"timeFrame": "09:50:00", "displayTime": "9:50 AM"},
    {"timeFrame": "09:55:00", "displayTime": "9:55 AM"},

    {"timeFrame": "10:20:00", "displayTime": "10:20 AM"},

    {"timeFrame": "10:30:00", "displayTime": "10:30 AM"},
    {"timeFrame": "10:35:00", "displayTime": "10:35 AM"},
    {"timeFrame": "10:40:00", "displayTime": "10:40 AM"},
    {"timeFrame": "10:45:00", "displayTime": "10:45 AM"},

    {"timeFrame": "11:20:00", "displayTime": "11:20 AM"},

    {"timeFrame": "11:30:00", "displayTime": "11:30 AM"},
    {"timeFrame": "11:35:00", "displayTime": "11:35 AM"},
    {"timeFrame": "11:40:00", "displayTime": "11:40 AM"},

    {"timeFrame": "11:55:00", "displayTime": "11:55 AM"},
    {"timeFrame": "12:00:00", "displayTime": "12:00 PM"},
    {"timeFrame": "12:05:00", "displayTime": "12:05 PM"},
    {"timeFrame": "12:10:00", "displayTime": "12:10 PM"},
    {"timeFrame": "12:15:00", "displayTime": "12:15 PM"},

    {"timeFrame": "12:20:00", "displayTime": "12:20 PM"},
    {"timeFrame": "12:25:00", "displayTime": "12:25 PM"},
    {"timeFrame": "12:30:00", "displayTime": "12:30 PM"},
    {"timeFrame": "12:35:00", "displayTime": "12:35 PM"},
    {"timeFrame": "12:40:00", "displayTime": "12:40 PM"},

    {"timeFrame": "13:20:00", "displayTime": "1:20 PM"},
    {"timeFrame": "13:25:00", "displayTime": "1:25 PM"},
    {"timeFrame": "13:30:00", "displayTime": "1:30 PM"},
    {"timeFrame": "13:35:00", "displayTime": "1:35 PM"},
    {"timeFrame": "13:40:00", "displayTime": "1:40 PM"},

    {"timeFrame": "14:20:00", "displayTime": "2:20 PM"},
    {"timeFrame": "14:25:00", "displayTime": "2:25 PM"},
    {"timeFrame": "14:30:00", "displayTime": "2:30 PM"},
    {"timeFrame": "14:35:00", "displayTime": "2:35 PM"},
    {"timeFrame": "14:40:00", "displayTime": "2:40 PM"}
]


# Function to process each time frame
def process_time_frame(timeFrameForOneTwenty, displayTimeFor120):
    while True:
        current_time = datetime.now().strftime("%H:%M:%S")

        # Check if the current time matches the scheduled time frame
        if current_time == timeFrameForOneTwenty:
            print(f"Processing {timeFrameForOneTwenty} at {current_time}")
            oneTwenty.checkOneTwentyReversal(access_token, base_url, headers, instrument_keys, timeFrameForOneTwenty,
                                             displayTimeFor120)
            break  # Stop the loop after processing

        else:
            # Calculate the time to wait until the target time
            target_time = datetime.strptime(timeFrameForOneTwenty, "%H:%M:%S")
            current_time_obj = datetime.strptime(current_time, "%H:%M:%S")
            time_to_wait = (target_time - current_time_obj).total_seconds()

            if time_to_wait > 0:
                # Sleep until the scheduled time
                print(f"Waiting until {timeFrameForOneTwenty} (remaining {time_to_wait} seconds)\n")

                tm.sleep(time_to_wait)  # Sleep until the exact scheduled time
            else:
                # Skip if the scheduled time has passed
                print(f"Missed {timeFrameForOneTwenty}, moving to the next time frame.")
                break  # Exit the loop if the time is missed


# Create a thread for each time frame
threads = []
for timeFrame in timeFrames:
    timeFrameForOneTwenty = timeFrame["timeFrame"]
    displayTimeFor120 = timeFrame["displayTime"]

    # Create a new thread for each time frame
    thread = threading.Thread(target=process_time_frame, args=(timeFrameForOneTwenty, displayTimeFor120))
    threads.append(thread)

# Start all threads
for thread in threads:
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()
