import requests
from urllib.parse import urljoin
# from pprint import pprint


class YandexMetrika(object):
    _METRIKA_STAT_URL = 'https://api-metrika.yandex.ru/stat/v1/'
    _METRIKA_MANAGEMENT_URL = 'https://api-metrika.yandex.ru/management/v1/'
    token = None

    def __init__(self, token):
        self.token = token

    def _get_header(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token),
            'User-Agent': 'myself'
        }

    def counters(self):
        url = urljoin(self._METRIKA_MANAGEMENT_URL, 'counters')
        headers = self._get_header()
        response = requests.get(url, headers=headers)
        counter_list = [c['id'] for c in response.json()['counters']]
        return counter_list

    def visits(self, counter_id):
        url = urljoin(self._METRIKA_STAT_URL, 'data')
        headers = self._get_header()
        params = {
            'id': counter_id,
            'metrics': 'ym:s:visits'
        }
        response = requests.get(url, params, headers=headers)
        #         print(response.headers['Content-Type'])
        #         pprint(response.json())
        visits_count = int(response.json()['data'][0]['metrics'][0])
        return visits_count

    def views(self, counter_id):
        url = urljoin(self._METRIKA_STAT_URL, 'data')
        headers = self._get_header()
        params = {
            'id': counter_id,
            'metrics': 'ym:pv:pageviews'
        }
        response = requests.get(url, params, headers=headers)
        #         print(response.headers['Content-Type'])
        #         pprint(response.json())
        views_count = int(response.json()['data'][0]['metrics'][0])
        return views_count

    def visitors(self, counter_id):
        url = urljoin(self._METRIKA_STAT_URL, 'data')
        headers = self._get_header()
        params = {
            'id': counter_id,
            'metrics': 'ym:s:users'
        }
        response = requests.get(url, params, headers=headers)
        #         print(response.headers['Content-Type'])
        #         pprint(response.json())
        visitors_count = int(response.json()['data'][0]['metrics'][0])
        return visitors_count


my_URL = 'www.sokolovdp.info'

with open('metrika_token.txt', 'r') as f:
    mytoken = f.read().strip()

ymetrika = YandexMetrika(mytoken)

counters = ymetrika.counters()
print("list of my counters:", counters)

visits = ymetrika.visits(counters[0])
views = ymetrika.views(counters[0])
visitors = ymetrika.visitors(counters[0])
print('my site {}  visited {}  and  viewed {} times by {} unique visitors'.format(my_URL, visits, views, visitors))
