import datetime
import json
import requests
import time
import tweet


base_url = 'https://www.recreation.gov/api/camps/availability/campground/'
# Specify a browser to the endpoint just so it agrees
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def main():
    target_campgrounds = [
        232470,
        232472,
        232473,
        272299,
        272300,
        10056207
    ]

    # Set is used instead of list for faster lookup performance
    # Also we don't want repeats.
    target_dates = {
        datetime.datetime(2020, 11, 13),
        datetime.datetime(2020, 11, 14),
        datetime.datetime(2020, 11, 15)
    }

    unique_months = get_unique_months(target_dates)

    discovered_campgrounds = {}

    for campground_id in target_campgrounds:
        target_url = base_url + str(campground_id) + '/month'

        for unique_month in unique_months:
            # ISO 8601 datetime format
            year = unique_month[0]
            month = unique_month[1]
            

            date_param = datetime.datetime(
                year=year,
                month=month,
                day=1
            ).isoformat() + '.000Z'

            payload = {
                'start_date': str(date_param)
            }

            r = requests.get(target_url, params=payload, headers=headers)
            response_dict = r.json()

            # {"campsites": ..., "count": ...}
            campsites_dict = response_dict["campsites"]

            discovered_campsites = {}

            for campsite_id in campsites_dict.keys():
                discovered_days = []

                campsite = campsites_dict[campsite_id]
                availabilities = campsite["availabilities"]

                for key in availabilities.keys():
                    iso_date = datetime.datetime.fromisoformat(key[:-1])
                    #formatted_date = iso_date.date()
                    formatted_date = datetime.datetime(
                        iso_date.year,
                        iso_date.month,
                        iso_date.day
                    )

                    if formatted_date in target_dates:
                        status = availabilities[key]
                        
                        if status == "Available":
                            # Add discovered date to campsite
                            discovered_days.append(formatted_date.date())

                # Add any discovered dates to campsite dictionary
                if discovered_days:
                    discovered_campsites[campsite_id] = discovered_days

            # Add any discovered campsites to campground dictionary
            if discovered_campsites:
                discovered_campgrounds[campground_id] = discovered_campsites
                
    message = build_alert_message(discovered_campgrounds)
    tweet.tweet_message(message)


def get_unique_months(target_dates):
    # Generate dictionary of year-month to days. We need to do this because api returns
    # data by month.
    unique_months = {}
    for item in target_dates:
        key = (item.year, item.month)
        if key in unique_months:
            unique_months[key].append(item.day)
        else:
            unique_months[key] = [item.day]
    
    return unique_months


def build_alert_message(campgrounds):
    alert_message = ""

    for campground_id in campgrounds:
        alert_message += ("Campground " + str(campground_id) + ", go to: https://www.recreation.gov/camping/campgrounds/" + str(campground_id) + "\n")
        campsites = campgrounds[campground_id]

        for campsite_id in campsites:
            alert_message += ("Campsite " + str(campsite_id) + ": ")            
            alert_message += ", ".join([str(date) for date in campsites[campsite_id]])
            alert_message += "\n"

    return alert_message


if __name__ == "__main__":
    start = time.time()

    main()

    end = time.time()

    print("Elapsed time: ", end - start)
