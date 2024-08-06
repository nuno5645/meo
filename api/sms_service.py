import requests
from django.conf import settings
from urllib.parse import quote
import requests

class NotificationService:
    PUSHOVER_API_URL = "https://api.pushover.net/1/messages.json"
    TEXTMEBOT_API_URL = "http://api.textmebot.com/send.php"

    def __init__(self):
        self.pushover_user_key = settings.PUSHOVER_USER_KEY
        self.pushover_api_token = settings.PUSHOVER_API_TOKEN
        self.textmebot_api_key = settings.TEXTMEBOT_API_KEY

    def send_pushover(self, message, title=None, url=None, priority=0, device=None, sound=None):
        payload = {
            "token": self.pushover_api_token,
            "user": self.pushover_user_key,
            "message": message,
            "priority": priority
        }

        if title:
            payload["title"] = title
        if url:
            payload["url"] = url
        if device:
            payload["device"] = device
        if sound:
            payload["sound"] = sound

        response = requests.post(self.PUSHOVER_API_URL, data=payload)

        if response.status_code == 200:
            print("Pushover notification sent successfully!")
            return True, response.json()
        else:
            print(f"Failed to send Pushover notification. Status code: {response.status_code}")
            print(response.text)
            return False, None

    def send_sms(self, phone_number, message):
        encoded_message = quote(message)
        url = f"{self.TEXTMEBOT_API_URL}?recipient={phone_number}&apikey={self.textmebot_api_key}&text={encoded_message}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            if "Success" in response.text:
                print("SMS sent successfully!")
                return True, "Message sent successfully"
            else:
                print(f"Failed to send SMS: {response.text}")
                return False, f"Failed to send message: {response.text}"
        except requests.RequestException as e:
            print(f"Error sending SMS: {str(e)}")
            return False, f"Error sending message: {str(e)}"

    def validate_pushover_user(self, device=None):
        validate_url = "https://api.pushover.net/1/users/validate.json"
        payload = {
            "token": self.pushover_api_token,
            "user": self.pushover_user_key
        }
        if device:
            payload["device"] = device

        response = requests.post(validate_url, data=payload)

        if response.status_code == 200:
            result = response.json()
            if result.get("status") == 1:
                print("Pushover user validated successfully!")
                print("Active devices:", result.get("devices"))
            else:
                print("Pushover user validation failed.")
            return result
        else:
            print(f"Failed to validate Pushover user. Status code: {response.status_code}")
            print(response.text)
            return None