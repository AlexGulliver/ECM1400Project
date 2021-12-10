from covid_news_handling import news_API_request
from covid_news_handling import update_news
from covid_news_handling import key

def test_news_API_request():
    assert news_API_request(key, 'gb') is not None

def test_update_news():
    update_news()
