import requests
import schedule
import time
import os
from urllib.parse import quote

def fetch_prayer_times(city, country):
    encoded_city = quote(city)
    encoded_country = quote(country)
    api_url = f"http://api.aladhan.com/v1/timingsByCity?city={encoded_city}&country={encoded_country}&method=2"
    response = requests.get(api_url)
    data = response.json()
    times = data['data']['timings']
    return times  # Returns a dictionary of prayer times

def schedule_fixed_fajr_adhan():
    # Set the Fajr time to 5:27
    schedule.every().day.at("05:27").do(play_adhan, "Fajr")

def play_adhan(prayer):
    print(f"It's time for {prayer} prayer.")
    os.system(f'afplay "/Users/mahmoudkassem/Downloads/Adhan.mp3"') 

def get_next_fajr(prayer_times):
    # Fixed Fajr time at 5:27
    fajr_time = "05:27"
    current_time = time.strftime("%H:%M")
    if fajr_time > current_time:
        return f"The next Fajr prayer is at {fajr_time}."
    else:
        return "No more Fajr prayers for today."

def run():
    city = "Abu Dhabi"  # Replace with your city
    country = "United Arab Emirates"  # Replace with your country
    # Override Fajr time with a fixed time
    prayer_times = fetch_prayer_times(city, country)
    prayer_times["Fajr"] = "05:27"
    
    schedule_fixed_fajr_adhan()

    while True:
        schedule.run_pending()
        next_fajr_info = get_next_fajr(prayer_times)
        print(next_fajr_info)
        time.sleep(1)

if __name__ == "__main__":
    run()
