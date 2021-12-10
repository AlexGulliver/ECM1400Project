"""This module is designed to handle COVID data in the form of a static csv file for dashboard
applications.
@Author: Alex Gulliver
@Updated: """

import csv
import sched
import time

s = sched.scheduler(time.time, time.sleep)

def parse_csv_data(csv_filename)-> list:
    """Opens csv covid data file and converts to a list."""
    with open(csv_filename, 'r', encoding = 'utf-8') as file:
        data = csv.reader(file, delimiter=',')
        data_list = []
        skip = True
        for row in data:
            if skip:
                skip = False
                #Skips first line because it is the title line
            else:
                data_list.append(row)
        return data_list

def process_covid_csv_data(covid_csv_data)-> tuple:
    """Goes through the list and sums the total cases in the last 7 days (skipping past the
    first entry as the data will be incomplete for the day) and finds the daily figures for
    the current hospital cases and the culmulative deaths and returns them."""
    cases_last_7_days = 0
    current_hospital_cases = 0
    cum_deaths = 0
    days = 7
    for row in covid_csv_data[2:]:
        if row[6] != '' and days > 0:
            cases_last_7_days += int(row[6])
            days -= 1
    for row in covid_csv_data:
        if row[5] != '':
            current_hospital_cases = row[5]
            break
    for row in covid_csv_data:
        if row[4] != '':
            cum_deaths = row[4]
            break
    #print(cases_last_7_days, current_hospital_cases, cum_deaths)
    return(cases_last_7_days, current_hospital_cases, cum_deaths)

covid_data_list = (parse_csv_data('nation_2021-10-28.csv'))

(process_covid_csv_data(covid_data_list))
 