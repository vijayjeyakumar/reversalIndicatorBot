from datetime import datetime, timedelta
import telagramAPI as sendTelegramMsg
import fullMarketQuoteAPI as fullQuote
import OHLCAPI
from datetime import datetime, timedelta
import time as tm


def fetchHighLowIn5Mins(access_token, base_url, headers, instrument_keys, startingTimeFrameForNext5Mins):
    start_time = datetime.strptime(startingTimeFrameForNext5Mins, "%H:%M:%S")
    end_time = start_time + timedelta(minutes=5)

    # Dictionaries to store low and high values for each instrument's actual name
    low_high_values = {}

    while datetime.now().time() < end_time.time():
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"Current time in while loop of fetchHighLowIn5Mins: {current_time}")

        try:
            # Fetch OHLC data for all instruments in one call
            ohlcQuote = OHLCAPI.fetchOHLC(access_token, base_url, headers, instrument_keys)
            print(f"ohlc quote is {ohlcQuote}")

            # Process each instrument's data
            for instrument_key, data in ohlcQuote.get('data', {}).items():
                try:
                    # Skip if 'ohlc' is None or missing
                    if not data or 'ohlc' not in data or data['ohlc'] is None:
                        print(f"Invalid or missing OHLC data for instrument {instrument_key}. Skipping...")
                        continue

                    # Extract actual instrument name (if available, or fallback to key)
                    instrument_actual_name = data.get("symbol", instrument_key)

                    # Extract low and high values
                    low_value = data['ohlc']['low']
                    high_value = data['ohlc']['high']

                    # Ensure the instrument name is initialized in the dictionary
                    if instrument_actual_name not in low_high_values:
                        low_high_values[instrument_actual_name] = {"low": [], "high": []}

                    # Append the low and high values for the current instrument
                    low_high_values[instrument_actual_name]["low"].append(low_value)
                    low_high_values[instrument_actual_name]["high"].append(high_value)

                except KeyError as ke:
                    print(f"KeyError processing instrument {instrument_key}: {ke}")
                except TypeError as te:
                    print(f"TypeError processing instrument {instrument_key}: {te}")
                except Exception as e:
                    print(f"Unexpected error processing instrument {instrument_key}: {e}")

        except Exception as e:
            print(f"Error fetching OHLC data for instruments: {e}")

        tm.sleep(60)  # Wait for 1 minute before the next fetch

    # Calculate and return the lowest and highest values for each instrument
    low_high_summary = {
        name: {
            "low": min(values["low"]) if values["low"] else None,
            "high": max(values["high"]) if values["high"] else None
        }
        for name, values in low_high_values.items()
    }
    return low_high_summary


def checkOneTwentyReversal(access_token, base_url, headers, instrument_keys, timeFrameForOneTwenty, displayTimeFor120):
    # Fetch the full market quote
    fullMarketQuote = fullQuote.fetchFullMarketQuote(access_token, base_url, headers, instrument_keys)

    lowValuesBefore120 = {}
    highValuesBefore120 = {}

    # Extract low and high values before 120
    for instrument_key, data in fullMarketQuote['data'].items():
        lowValuesBefore120[instrument_key] = data['ohlc']['low']
        highValuesBefore120[instrument_key] = data['ohlc']['high']

    print("Low values before 120:", lowValuesBefore120)
    print("High values before 120:", highValuesBefore120)

    time_object = datetime.strptime(timeFrameForOneTwenty, "%H:%M:%S")
    time_object_plus_one = time_object + timedelta(minutes=1)
    startingTimeFrameForNext5Mins = time_object_plus_one.strftime("%H:%M:%S")

    while True:
        current_time = datetime.now().strftime("%H:%M:%S")
        if current_time >= startingTimeFrameForNext5Mins:
            print("Before calling FetchLowest and Highest values in 5 mins Function")
            # Fetch the lowest and highest values in the 5-minute window
            lowestValuesIn5Mins = fetchHighLowIn5Mins(access_token, base_url, headers, instrument_keys,
                                                      startingTimeFrameForNext5Mins)
            print("After calling fetch function")
            print("Lowest values in 5 minutes:", lowestValuesIn5Mins)

            # Compare and send notifications for both lows and highs
            for instrumentActualName in lowValuesBefore120.keys():
                lowValueOfTheDayBefore120 = lowValuesBefore120[instrumentActualName]
                highValueOfTheDayBefore120 = highValuesBefore120[instrumentActualName]

                # Fetch corresponding 5-minute values
                valuesInThe5minCandle = lowestValuesIn5Mins.get(instrumentActualName, {})
                lowestValueInThe5minscandle = valuesInThe5minCandle.get("low")
                highestValueInThe5minscandle = valuesInThe5minCandle.get("high")

                print(f"Lowest Value in the 5 mins candle for {instrumentActualName} is {lowestValueInThe5minscandle}")
                print(f"High Value in the 5 mins candle for {instrumentActualName} is {highValueOfTheDayBefore120}")

                # Send message for new low
                if lowestValueInThe5minscandle is not None and lowestValueInThe5minscandle <= lowValueOfTheDayBefore120:
                    sendTelegramMsg.sendMsg(
                        f"New Low has been formed in {displayTimeFor120} candle for {instrumentActualName}")

                # Send message for new high
                if highestValueInThe5minscandle is not None and highestValueInThe5minscandle >= highValueOfTheDayBefore120:
                    sendTelegramMsg.sendMsg(
                        f"New High has been formed in {displayTimeFor120} candle for {instrumentActualName}")
            break  # Break after processing the 5-minute window

        else:
            # Calculate sleep time until the next fetch
            start_time = datetime.strptime(startingTimeFrameForNext5Mins, "%H:%M:%S")
            current_time_obj = datetime.strptime(current_time, "%H:%M:%S")
            time_to_sleep = (start_time - current_time_obj).total_seconds()

            print(f"Waiting for {startingTimeFrameForNext5Mins} for all instruments...")
            tm.sleep(min(time_to_sleep, 5))
