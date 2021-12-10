"""This module is designed to take data from the uk-covid-19 module provided
by Public Health England. By default it will take covid 19 data from the city of Exeter.
@Author: Alex Gulliver
@Updated: 10/12/2021"""

import json
import logging
from typing import Any
from uk_covid19 import Cov19API

covid_figures = {}

logging.basicConfig(filename='sys.log', encoding='utf-8', level=logging.DEBUG)

england_only = [
    'areaType=nation',
    'areaName=England'
]

uk_data = [
    'areaType=all_nations',
    'structure=cases_and_deaths'
]

Exeter = [
    'areaType=ltla',
    'areaName=exeter'
]

cases_and_deaths = {
    "area_code": "areaCode",
    "area_name": "areaName",
    "area_type": "areaType",
    "date": "date",
    "cum_deaths": "cumDeaths28DaysByDeathDate",
    "hospital_cases": "hospitalCases",
    "new_cases": "newCasesByPublishDate"
}
# newCasesbyPublishDateRollingSum
# areaCode,areaName,areaType,date,cumDailyNsoDeathsByDeathDate,hospitalCases,newCasesBySpecimenDate

release_timestamp = Cov19API.get_release_timestamp()
logging.info('[%s]uk_covid_api_request | COV19 API release stamp: ' +
             release_timestamp)


def covid_API_request(location_type: str='ltla', location: str='Exeter') -> dict:
    """Requests data using default location of Exeter. Returns data as a dictionary."""
    filters_format = [
        'areaType=' + location_type,
        'areaName=' + location
    ]
    api = Cov19API(filters=filters_format, structure=cases_and_deaths)
    try:
        data = api.get_json()
        logging.info(
            "uk_covid_api_request | Data received from NHS API TIMESTAMP: " + release_timestamp)
        return data
    except:
        logging.error(
            "uk_covid_api_request | ERROR: Data not received from NHS API")


def process_data_weekly_infections(returned_data) -> Any:
    """Takes dictionary data and calculates the total new infections
    over the last 7 days. Skips the first day as usually the total
    number of new infections for a day is not finalised."""
    last_week_infections = 0
    days = 7
    skip = True
    list_of_dicts = (returned_data['data'])
    for diction in list_of_dicts:
        if skip:
            #Skips first day due to incomplete results for most recent day of data
            skip = False
        elif (diction['new_cases']) is not None and days > 0:
            last_week_infections += int(diction['new_cases'])
            days -= 1
    logging.info("uk_covid_api_request | weekly infections processed")
    return last_week_infections
    


def process_data_hospital(returned_data) -> Any:
    """Retreives number of hospital cases currently from data"""
    list_of_dicts = (returned_data['data'])
    logging.info("uk_covid_api_request | hospital cases processed")
    return list_of_dicts[1]['hospital_cases']


def process_data_deaths(returned_data) -> Any:
    """Retreives number of culmulative deaths from data"""
    list_of_dicts = (returned_data['data'])
    logging.info("uk_covid_api_request | death data processed")
    return list_of_dicts[1]['cum_deaths']


Exeter_Data = covid_API_request()
England_Data = covid_API_request('nation', 'england')

local_week_new_cases = str((process_data_weekly_infections(Exeter_Data)))
national_week_new_cases = str((process_data_weekly_infections(England_Data)))
hospital_cases_england = str((process_data_hospital(England_Data)))
cum_deaths_england = str((process_data_deaths(England_Data)))


def covid_data_to_file()-> None:
    """Used to update the covid figures. Clears json file first and then
    calls API to get the most recent figures and proceeds to place them
    inside a json file. """
    covid_figures["local_weekly_cases"] = local_week_new_cases
    covid_figures["national_weekly_cases"] = national_week_new_cases
    covid_figures["hospital_cases"] = hospital_cases_england
    covid_figures["cum_deaths"] = cum_deaths_england
    with open('covid_data', 'w', encoding = 'utf-8') as file:
        json.dump(covid_figures, file)
    logging.info("uk_covid_api_request | Covid data written to file")

covid_data_to_file()
