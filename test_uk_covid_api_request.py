from typing import Any
from uk_covid_api_request import covid_API_request
from uk_covid_api_request import process_data_weekly_infections
from uk_covid_api_request import process_data_hospital
from uk_covid_api_request import process_data_deaths

data = covid_API_request()

def test_covid_API_request():
    data = covid_API_request()
    assert isinstance(data, dict)

def test_process_data_weekly_infections():
    check = process_data_weekly_infections(data)
    assert isinstance(check, int)

def test_process_data_deaths():
    check2 = process_data_deaths(data)
    assert isinstance(check2, int)
