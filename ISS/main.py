import requests
import smtplib
from credentials import credentials
from datetime import datetime
import time

MY_LAT = 55.704659  # Lund latitude
MY_LONG = 13.191007  # Lund longitude
my_email = credentials["email"]
my_password = credentials["password"]

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])


def is_within():
    # My position is within +5 or -5 degrees of the ISS position.
    low_lat = MY_LAT - 5
    high_lat = MY_LAT + 5
    low_long = MY_LONG - 5
    high_long = MY_LONG + 5
    return low_lat <= iss_latitude <= high_lat and low_long <= iss_longitude <= high_long


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get(
    "https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()


def is_dark():
    hour = time_now.hour
    return hour < sunrise or hour > sunset


while True:
    time.sleep(120)
    if is_within() and is_dark():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_password)
            connection.sendmail(from_addr=my_email,
                                to_addrs="ponjae11@gmail.com", msg=f"Subject:ISS is above you!\n\nLook up in the sky it is located at {iss_latitude} {iss_longitude}")
