import os
import time
import requests
import boto3

from utils import to_string

"""
open close high low: https://analyzingalpha.com/open-high-low-close-stocks
"""


class Solver:

    def __init__(self) -> None:
        self.root_url = "https://query2.finance.yahoo.com//v8/finance/chart/{t}?symbol={t}&period1={s}&period2={e}&interval={i}"
        self.headers = {"user-agent": "..."} # add your used-agent here
        
        # CONNECTION STRINGS
        self.table_name = "market-table" # recommended table name
        self.access_key_id = "..." # AWS connection strings
        self.secret_access_key = "..." # AWS connection strings
        self.region_name = "us-east-1" # change this based on your DynamoDB region
        self.client = boto3.client(
            "dynamodb",
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name = self.region_name,
        )
        self.dynamodb = boto3.resource(
            "dynamodb",
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name = self.region_name,
        )

    def _scrape_step(self, ticker, start, end, interval="1m"):
        """Scrape Yahoo Finance price information

        Args:
            ticker (str): Ticker symbol for the desired stock
            start (int): Unix timestamp for the starting time
            end (int): Unix timestamp for the ending time
            interval (str): Desired interval of the ticks

        Returns:
            output_dict (dict): output dictionary, where all items are in format:
                {ticker-timestamp, low, close, high, volume, open}
        """
        query = self.root_url.format(t=ticker, s=start, e=end, i=interval)
        r = requests.get(query, headers=self.headers)
        data = r.json()
        timestamp = data["chart"]["result"][0]["timestamp"]
        low = data["chart"]["result"][0]["indicators"]["quote"][0]["low"]
        close = data["chart"]["result"][0]["indicators"]["quote"][0]["close"]
        high = data["chart"]["result"][0]["indicators"]["quote"][0]["high"]
        volume = data["chart"]["result"][0]["indicators"]["quote"][0]["volume"]
        open = data["chart"]["result"][0]["indicators"]["quote"][0]["open"]
        
        output_dict = {}
        for i, time in enumerate(timestamp):
            if time > end or time < start:
                continue
            val = ticker+"-"+str(time)
            output_dict[val] = {"ticker-timestamp":val, "low":str(low[i]), "close":str(close[i]), "high":str(high[i]), "volume":str(volume[i]), "open":str(open[i])}
        return output_dict

    def _upload_step(self, upload_dict):
        print("-- Uploading... --")
        for key in upload_dict:
            self.dynamodb.Table(self.table_name).put_item(
                Item=upload_dict[key]
            )
        print("-- Upload Successful --")

    def scrape_upload(self, ticker):
        """
        Steps of scraping:
        - check database for the last entry date, if last entry date yesterday -> 1, else -> 2
            - 1) scrape last days price information
            - 2) if last entry date do exist -> 2.1, else -> 2.2
                - 2.1) scrape data day by day until you reach today
                - 2.2) scrape data starting from start limit (constraint) until you reach today
        Steps of uploading to database
        - do it step by step to reduce the load
        """
        end_t = int(time.time())
        breaks = [] # time 
        for i in range(6): # go to the past up-to 10 days
            breaks.append(end_t - (86400*2*i))
        breaks = breaks[::-1]
        print("- Scrape-Upload starting from " , to_string(breaks[0]), " to ", to_string(breaks[-1]), " -")
        breaks[-1] += 1
        for step in range(len(breaks)-1):
            start, end = breaks[step], breaks[step+1]-1
            output_dict = self._scrape_step(ticker=ticker, start=start, end=end)
            self._upload_step(output_dict)
        print("- Scrape-Upload completed -")

        return

    def clean(self):
        """
        If the database contains outdated data, remove them (start limit), since we donot have unlimited space
        """
        pass

    def run(self):
        """
        Run funtion, which should be called daily --> performs scrape, upload, clean
        """
        pass