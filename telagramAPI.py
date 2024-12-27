import requests

# Hardcoded Values
bot_token = "7879346585:AAG3SfYaqWg6FpmbS10vZ4_y1VLhYl6nqwU"
chat_id = "-4632318077"
telegramSendMsgUrl = f"https://api.telegram.org/bot{bot_token}/sendMessage"


def sendMsg(data):
    # Generate payload & Send
    payload = {
        "chat_id": chat_id,
        "text": data
    }
    response = requests.post(telegramSendMsgUrl, json=payload)
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Error: {response.text}")
