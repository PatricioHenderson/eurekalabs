from django.http import HttpResponse, response
from rest_framework.decorators import api_view
from django.http import JsonResponse
import requests
import json

@api_view(['GET' , 'POST'])
def signup(request):
    template = '<h1>Hello, {0}!</h1>'
    return HttpResponse(template)


@api_view(['GET' , 'POST'])
def stock_information(request):
    '''
    API VIEW to get stock information
    '''
    open_price = []
    high_price = []
    low_price = []
    variation = []
    json_data = {}

    simbol = 'FB' #request.get('simbol')
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + simbol + '&outputsize=compact&apikey=X86NOH6II01P7R24'
    response = requests.get(url).json()
    def get_response_info(response):
        '''
        In this function we get the response from the API and we store it in a list
        '''
        for key, value in response.items():
            if key == 'Time Series (Daily)':
                for key, value in value.items():
                    open_price.append(value['1. open'])
                    high_price.append(value['2. high'])
                    low_price.append(value['3. low'])
                    variation.append(value['4. close'])
        return open_price, high_price, low_price, variation
    get_response_info(response)
    
    def info_json(open_price, high_price, low_price, variation):
        '''
        This is the first step to convert the list into a json file
        We need a dictionary to store the information
        '''
        json_data['open_price'] = open_price
        json_data['high_price'] = high_price
        json_data['low_price'] = low_price
        json_data['variation'] = variation
        return json_data
    info_json(open_price, high_price, low_price, variation)

    data = []
    def create_json():
        '''
        Finally we create a json file with the information obtained from the request
        '''
        for i in range(len(open_price)):
            data.append({
                'open_price': open_price[i],
                'high_price': high_price[i],
                'low_price': low_price[i],
                'variation': variation[i]
            })
    create_json()

    info = {
        simbol : data
    }
    return JsonResponse(info)



