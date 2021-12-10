"""This module is designed to take covid-related news articles from the News
API using keywords (default to : Covid, COVID-19 and coronavirus.)
@Author: Alex Gulliver
@Updated: 10/12/2021"""

import json
import logging
import requests
from time_conversions import current_time

article_title_list = []
article_description_list = []

logging.basicConfig(filename='sys.log', encoding='utf-8', level=logging.DEBUG)

with open('config.json', 'r', encoding = 'utf-8') as file:
    json_file = json.load(file)
    keys = json_file["API-keys"]
    key = (keys["news"])
    configs = json_file["Configuration"]
    set_country = (configs["country"])

def news_API_request(
	config_key: str, country_setting: str, covid_terms=["Covid", "COVID-19", "coronavirus"]) -> tuple:
    """Calls the NewsAPI and returns a list of the article titles
	and a list of the article content."""
    base_url = "https://newsapi.org/v2/top-headlines?"
    api_key = config_key
    country = country_setting
    complete_url = base_url + "country=" + country + "&apiKey=" + api_key
    response = requests.get(complete_url)
    news_raw_data = response.json()
    logging.info(
        'covid_news_handling | news_API_request REQUEST at: ' + current_time)
    for article in (news_raw_data['articles']):
        matches = covid_terms
        if any(x in article['title'] for x in matches):
            article_title_list.append(article['title'])
            article_description_list.append(article['description'])
    return article_title_list, article_description_list

data = news_API_request(key, set_country)

def update_news() -> tuple:
	"""Updates news articles"""
	new_story_titles = []
	new_story_descriptions = []
	new_story_titles.append(data)
	logging.info("covid_news_handling | News articles updated")
	return new_story_titles, new_story_descriptions

update_news()
