import requests


class RandomNumberConnector:
    def __init__(self):
        self._url =  "http://www.randomnumberapi.com/api/v1.0/random"
        self._min = 0
        self._max = 1000
        self._count = 1
        
    def __get_params(self):
        return {
            "min": self._min,
            "max": self._max,
            "count": self._count,
        }

    def get_number(self, **kwargs):
        url = self._url
        params = self.__get_params()
        response = requests.get(
            url, params=params
        )
        return response.json()[0]