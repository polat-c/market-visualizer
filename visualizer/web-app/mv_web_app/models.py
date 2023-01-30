from django.db import models

import time
import datetime
import requests
from getuseragent import UserAgent

class Ticker(models.Model):
    
    ticker = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.ticker} ({self.name})'

    def get_price_info(self, start_t=None, end_t=None, interval=None):
        """Getting the price tarjectories from start_t to end_t, if they are not given
        get the price trajectories of the past 5 days instead
        """
        if (not start_t) or (not end_t):
            end_t = int(time.time())
            start_t = end_t - (86400*5)
        else:
            end_t = time.mktime(end_t.timetuple())
            start_t = time.mktime(start_t.timetuple())
            # end_t = time.mktime(datetime.datetime.strptime(end_t, "%d/%m/%Y").timetuple())
            # start_t = time.mktime(datetime.datetime.strptime(start_t, "%d/%m/%Y").timetuple())
            end_t, start_t = int(end_t), int(start_t)
        if not interval:
            interval = "1m"
        return self._get_price_info(start_t, end_t, interval)

    def _get_price_info(self, start_t, end_t, interval):
        root_url = "https://query2.finance.yahoo.com//v8/finance/chart/{t}?symbol={t}&period1={s}&period2={e}&interval={i}"
        query = root_url.format(t=self.ticker, s=start_t, e=end_t, i=interval)
        
        useragent = UserAgent()
        theuseragent = useragent.Random()
        headers = {"user-agent": theuseragent}

        r = requests.get(query, headers=headers)
        data = r.json()
        return data
