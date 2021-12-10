"""This module is designed to allow the user to set and cancel updates for
coronavirus related news stories and coronavirus data in an interface.
@Author: Alex Gulliver
@Updated: 10/12/2021"""

import sched
import time
import json
import logging

from typing import Any
from flask import Flask, render_template, request, redirect
from time_conversions import hhmm_to_seconds, current_time
from covid_news_handling import news_API_request
from uk_covid_api_request import covid_data_to_file

app = Flask(__name__)

s = sched.scheduler(time.time, time.sleep)
news_schedule = sched.scheduler(time.time, time.sleep)
covid_schedule = sched.scheduler(time.time, time.sleep)
news_schedule_delete = sched.scheduler(time.time, time.sleep)
covid_schedule_delete = sched.scheduler(time.time, time.sleep)
covid_data_to_file()

with open('config.json', 'r', encoding = 'utf-8') as file:
    json_file = json.load(file)
    keys = json_file["API-keys"]
    key = (keys["news"])
    configs = json_file["Configuration"]
    set_country = (configs["country"])

logging.basicConfig(filename='sys.log', encoding='utf-8', level=logging.DEBUG)

data = news_API_request(key, set_country)
news_data = data[0]
news = []
schedule_toasts = []

def initial_news_articles(articles_to_load: tuple) -> Any:
    """Loads the currently available news articles pulled via the API so they are shown
    on the interface"""
    num_of = (len(articles_to_load[0]))
    num = (num_of) / 2
    # As there are two seperate lists one for titles and one for content, the length
    # of the entire list in half is equal to the amount of news articles. 
    count = 0
    while count < num:
        with open('deleted_news', encoding = 'utf-8') as myfile:
            if data[0][count] not in myfile.read():
                news.append({
                    "title": data[0][count],
                    "content": data[1][count]
                },)
        count += 1

initial_news_articles(data)

def update_news() -> None:
    """Wipes existing news and recalls news API. Checks news articles against
    the recorded deleted ones and also artilces that were being displayed."""
    count = 0
    current_news_titles = []
    for dictionary in news:
        current_news_titles.append(dictionary['title'])
    title_list = data[0]
    with open('deleted_news', encoding = 'utf-8') as myfile:
        for i in title_list:
            if i not in (myfile.read and current_news_titles):
                news.append({
                    "title": data[0][count],
                    "content": data[1][count]
                },)
            count += 1

def update_covid() -> None:
    """Wipes covid data and recalls NHS API for up to date coronavirus figures"""
    with open('covid_data', encoding = 'utf-8') as json_file:
        covid_data_to_file()

def schedule_covid_updates(update_interval : int, update_name : str) -> sched.Event:
    """Schedules a covid update and generates new covid data to be uploaded to the interface"""
    logging.info("flask_interface | Covid update set")
    update = covid_schedule.enter(update_interval, 1, update_covid)
    return update

def schedule_news_update(update_interval: int, update_name: str) -> sched.Event:
    """Takes update name and interval for news article from interface"""
    logging.info("flask_interface | News update set for: " +
                 str(update_interval) + " Name: " + update_name)
    update = news_schedule.enter(update_interval, 1, update_news)
    return update

def check_repeat() -> Any:
    """Checks to see if the repeat tickbox has been ticked"""
    will_repeat = request.args.get('repeat')
    if will_repeat:
        return True
    else:
        return False

def check_covid() -> Any:
    """Checks to see if the covid tickbox has been ticked"""
    will_repeat = request.args.get('covid-data')
    logging.info('flask_interface | covid-data REQUEST at: ' + current_time)
    if will_repeat:
        return True
    else:
        return False

def check_news() -> Any:
    """Checks to see if the news tickbox has been ticked"""
    will_repeat = request.args.get('news')
    logging.info('flask_interface | news REQUEST at: ' + current_time)
    if will_repeat:
        return True
    else:
        return False

def schedule_add_toast(
    up_time: int, up_label: str, new_covid: Any, new_news: Any, will_repeat: Any) -> Any:
    """When the user inputs something into the update label box, the function will reqeust it
    and evaluate which toasts to add to the scheduler and what to scheduler based on ther users
    inputs."""
    update_time = request.args.get('update')
    logging.info('flask_interface | update REQUEST at: ' + current_time)
    logging.info('flask_interface | Schedule set for ' + str(update_time))
    if new_covid and will_repeat:
        logging.info("COVID REPEATING schedule set")
        schedule_toasts.append({
            "title": "COVID | " + up_label,
            "content": "REPEATING Covid update set for: " + str(update_time)},)
        schedule_covid_updates(up_time, up_label)
        repeat_time = int(up_time) + 86400
        schedule_covid_updates(up_time, repeat_time)
    if new_news and will_repeat:
        logging.info("NEWS REPEATING schedule set")
        schedule_toasts.append({
            "title": "NEWS | " + up_label,
            "content": "REPEATING News update set for: " + str(update_time)},)
        schedule_news_update(up_time, up_label)
        repeat_time = int(up_time) + 86400
        schedule_covid_updates(up_time, repeat_time)
    if new_covid and not will_repeat:
        logging.info("COVID schedule set")
        schedule_toasts.append({
            "title": "COVID | " + up_label,
            "content": "Covid update set for: " + str(update_time)},)
        schedule_covid_updates(up_time, up_label)
    if new_news and not will_repeat:
        logging.info("NEWS schedule set")
        schedule_toasts.append({
            "title": "NEWS | " + up_label,
            "content": "News update set for: " + str(update_time)},)
        schedule_news_update(up_time, up_label)

def delete_schedule_toast() -> None:
    """Detects when the user clicks to delete a
    toast widget and removes that toast from the dashboard"""
    module_to_remove = request.args.get('update_item')
    logging.info('flask_interface | update_item REQUEST at: ' + current_time)
    print(module_to_remove)
    for item in schedule_toasts:
        if module_to_remove == item['title']:
            schedule_toasts.remove(item)

def delete_news_toast() -> list:
    """Detects when the user clicks to delete a toast widget
     and removes that article from the dashboard."""
    mod_to_remove = request.args.get('notif')
    logging.info('flask_interface | notif REQUEST at: ' + current_time)
    #news_values = news[0]
    for dictionary in news:
        if mod_to_remove == dictionary['title']:
            news.remove(dictionary)
            blacklist = open("deleted_news", "a", encoding = 'utf-8')
            blacklist.write(dictionary['title'])
            return news

@app.route('/')
def redirection():
    """This function redirects the user to the /index page"""
    return redirect('/index', code=302)

@app.route('/index')
def hello():
    """Main interface function. Returns a template with all covid data on. """
    # s.run(blocking=False)
    logging.info("MAIN Interface loaded")
    delete_news_toast()
    delete_schedule_toast()
    with open('covid_data', 'r', encoding = 'utf-8') as file_covid:
        covid_json = json.load(file_covid)
        l7di = covid_json['local_weekly_cases']
        n7di = covid_json['national_weekly_cases']
        hospital = covid_json['hospital_cases']
        deaths = covid_json['cum_deaths']
    try:
        text_field = request.args.get('two')
        logging.info('flask_interface | two REQUEST at: ' + current_time)
        update_time = request.args.get('update')
        logging.info('flask_interface | update REQUEST at: ' + current_time)
        if text_field:
            alarm_hhmm = update_time[-5:-3] + ':' + update_time[-2:]
            logging.info('flask_interface | Schedule set for ' + alarm_hhmm)
            delay = hhmm_to_seconds(alarm_hhmm) - hhmm_to_seconds(current_time)
            schedule_add_toast(delay, text_field, check_news(),
                               check_covid(), check_repeat())
        return render_template('index.html',
                               image='image.png',
                               title='Covid-19 Dashboard',
                               location='Exeter',
                               local_7day_infections=l7di,
                               nation_location='England',
                               national_7day_infections=n7di,
                               hospital_cases='National hospital cases: ' + hospital,
                               deaths_total='National culmulative deaths: ' + deaths,
                               news_articles=news,
                               updates=schedule_toasts,
                               )
    except:
        logging.exception('flask_interface | APP - route /index failed')

if __name__ == '__main__':
    app.run()
