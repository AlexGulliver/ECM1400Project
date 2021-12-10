from flask_interface import schedule_add_toast, schedule_covid_updates
from flask_interface import initial_news_articles
from flask_interface import schedule_news_update
from flask_interface import schedule_add_toast

def test_schedule_covid_updates():
    schedule_covid_updates(update_interval=10, update_name='update test')

def test_initial_news_articles():
    assert initial_news_articles is not None

def test_schedule_news_update():
    schedule_news_update(update_interval=10, update_name='update test')
