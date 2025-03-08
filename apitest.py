import requests
from bs4 import BeautifulSoup


def get_hko_weather_forecast():
    # request URL
    url = "https://pda.weather.gov.hk/locspc/data/fnd_uc.xml"

    # send request
    response = requests.get(url)

    # test if it's successful or not
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # get the body
        html_string = response.json()
        print(soup.prettify())

        # get max and min humidity of the day after tomorrow (n = 1)
        max_rh = html_string['forecast_detail'][1]['max_rh']
        min_rh = html_string['forecast_detail'][1]['min_rh']
        return f"The humidity range of the day after tomorrow is {min_rh} - {max_rh} %"
    else:
        return f"Request failed, the status code is {response.status_code}"


# run and print
print(get_hko_weather_forecast())
