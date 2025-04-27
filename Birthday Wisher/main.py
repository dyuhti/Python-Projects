import datetime as dt
import smtplib
import random
MY_EMAIL = "*****"
MY_PASSWORD = "*****"


now = dt.datetime.now()
day_of_week = now.weekday()
if day_of_week == 6:
    with open("./quotes.txt") as quote_file:
        all_quotes = quote_file.readlines()
        quote = random.choice(all_quotes)

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject:Quote of the day\n\n{quote}"
        )
