from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from .models import Ticker
from .forms import TickerForm
from .serializers import TickerSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .utils import get_figure

def market_data(request):
    data = Ticker.objects.all()
    return render(request, 'market_data/market_data.html', {'market_data': data})

def home(request):
    return HttpResponse("Homepage")

def detail(request, id):
    """
    Similar to JavaFX
    """
    data = Ticker.objects.get(pk=id) # pk: primary key
    return render(request, 'market_data/detail.html', {'ticker':data})

def add(request):
    ticker = request.POST.get('ticker')
    name = request.POST.get('name')

    if ticker and name:
        ticker = Ticker(ticker=ticker, name=name)
        ticker.save()
        return HttpResponseRedirect('/market_data')

    return render(request, 'market_data/add.html')

def delete(request, id):
    try:
        ticker = Ticker.objects.get(pk=id)
    except:
        raise Http404('Ticker does not exist')
    ticker.delete()
    return HttpResponseRedirect('/market_data')

###################################
###################################

@api_view(['GET', 'POST'])
def ticker_list(request):
    """ get all tickers
    serialize them
    return json
    """
    if request.method == "GET":
        tickers = Ticker.objects.all()
        serializer = TickerSerializer(tickers, many=True) # many arg means serialize all-o-them
        return JsonResponse({'tickers': serializer.data}, safe=False)
    if request.method == "POST":
        serializer = TickerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

###################################
###################################

def visualize(request):

    figure = None

    # ticker = request.POST.get('ticker')
    # name = request.POST.get('name')

    # start_t = request.POST.get('start_t')
    # end_t = request.POST.get('end_t')

    # interval = request.POST.get('interval')

    # if ticker and name:
    #     ticker = Ticker(ticker=ticker, name=name)
    #     data = ticker.get_price_info(start_t, end_t, interval)
    #     figure = get_figure(data)

    form = TickerForm(request.POST)

    if form.is_valid():
        ticker = form.cleaned_data['ticker']
        name = form.cleaned_data['name']
        start_t = form.cleaned_data['start_t']
        end_t = form.cleaned_data['end_t']
        interval = form.cleaned_data['interval']

        ticker = Ticker(ticker=ticker, name=name)
        data = ticker.get_price_info(start_t, end_t, interval)
        figure = get_figure(data)

    context = {
        'figure': figure
    }

    return render(request, 'visualize/plot.html', context)
