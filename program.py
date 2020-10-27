import datetime
import requests
import time


def main():
    base_url = 'https://www.recreation.gov/api/camps/availability/campground/'
    
    # Specify a browser to the endpoint
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    target_campgrounds = [
        232470,
        232473,
        272299,
        232472,
        10056207,
        272300
    ]

    target_dates = [
        datetime.datetime(2020, 11, 13),
        datetime.datetime(2020, 11, 14),
        datetime.datetime(2020, 11, 15)
    ]




    for campground_id in target_campgrounds:
        target_url = base_url + str(campground_id) + '/month'
        print(target_url)

        payload = {
            'start_date': '2020-11-01T00:00:00.000Z'
        }

        r = requests.get(target_url, params=payload, headers=headers)
        print(r.text)


if __name__ == "__main__":
    start = time.time()

    main()

    end = time.time()

    print("Elapsed time: ", end - start)
