import requests
from json import loads
NEWS_API_ENDPOINT = 'https://newsapi.org/v1/'
NEWS_API_KEY = '54066047f92c44b4b8082950968ea989'
ARTICALS_API = 'articles'

CNN = 'cnn'
default_SOURCES = [CNN]
SORT_BY_TOP = 'top'


def buildUrl(end_point=NEWS_API_ENDPOINT,api_name=ARTICALS_API):
    return end_point+api_name


def getNewsFromSource(sources=default_SOURCES,sortBy=SORT_BY_TOP):
    articles = []
    for source in sources:
        payload = {'apiKey':NEWS_API_KEY,
                    'source':source,
                    'sortBy':sortBy}
        response = requests.get(buildUrl(),params=payload)
        res_json = loads(response.content)

        if(res_json is not None and
           res_json['status'] == 'ok' and
           res_json['source'] is not None):

           for news in res_json['articles']:
               news['source'] = source

           articles.extend(res_json['articles'])
    return articles
