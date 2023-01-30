"""
Visualization utils
"""
import uuid, base64
from .models import *
from io import BytesIO

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def visualize(data_dict):

    price_data = data_dict["chart"]["result"][0]["indicators"]["quote"][0]
    high, low = price_data["high"], price_data["low"]
    x = np.arange(len(high))

    timestamps = data_dict["chart"]["result"][0]["timestamp"]
    start, end = timestamps[0], timestamps[-1]
    start, end = map(lambda i: datetime.utcfromtimestamp(i).strftime('%Y-%m-%d %H:%M:%S'), [start, end])

    plt.figure(figsize=(12,8))
    plt.plot(x, high, "-r", label="high")
    plt.plot(x, low, "-b", label="low")
    plt.legend(loc="best")
    plt.title("from {start} to {end}".format(start=start, end=end))
    plt.show()

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_figure(data, **kwargs):

    price_data = data["chart"]["result"][0]["indicators"]["quote"][0]
    high, low = price_data["high"], price_data["low"]
    x = np.arange(len(high))

    timestamps = data["chart"]["result"][0]["timestamp"]
    start, end = timestamps[0], timestamps[-1]
    start, end = map(lambda i: datetime.utcfromtimestamp(i).strftime('%Y-%m-%d %H:%M:%S'), [start, end])

    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(12, 8))
    plt.plot(x, high, "-r", label="high")
    plt.plot(x, low, "-b", label="low")
    plt.legend(loc="best")
    plt.title("from {start} to {end}".format(start=start, end=end))

    plt.tight_layout()
    figure = get_graph()
    return figure