"""
Going from a python object to JSON
"""
from rest_framework import serializers
from .models import Ticker

class TickerSerializer(serializers.ModelSerializer):
    class Meta:
        """ meta-data describing the model
        """
        model = Ticker
        fields = ['id', 'ticker', 'name']
        