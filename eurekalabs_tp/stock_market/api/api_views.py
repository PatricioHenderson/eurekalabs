from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import requests



class LoginUserAPIView(APIView):
    '''
    Input schema:
    {"username":"root", "last_name":"stanley" , "email":"test@email.com"}

    '''

    parser_classes = [MultiPartParser,FormParser,JSONParser]
    authentication_classes = []
    permission_classes = []

    def post(self, request,format=None):
        user_data = {}
        try:

            username = request.POST['username']
            last_name = request.POST['last_name']
            email = request.POST['email']


            user = User.objects.create_user(username, email, last_name)
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            
            user['token'] = token.key
            user.save()
            account = (username==username, last_name==last_name , email==email)


        except Exception as error:
            user_data['response'] = 'Error'
            user_data['error_message'] = str(error)
            return Response(user_data)                


@api_view(['GET' , 'POST'])
def stock_information(request):
    '''
    API VIEW to get stock information
    '''
    permission_classes = [IsAuthenticated]

    open_price = []
    high_price = []
    low_price = []
    close = []
    variation = [0]
    json_data = {}


    simbol = request.GET.get('simbol')
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + str(simbol) + '&outputsize=compact&apikey=X86NOH6II01P7R24'
    response = requests.get(url).json()
    def get_response_info(response):
        '''
        In this function we get the response from the API and we store it in a list)
        '''
        for key, value in response.items():
            if key == 'Time Series (Daily)':
                for key, value in value.items():
                    open_price.append(value['1. open'])
                    high_price.append(value['2. high'])
                    low_price.append(value['3. low'])
                    close.append(value['4. close'])
        return open_price, high_price, low_price, close
    get_response_info(response)


    def get_varation(close):
        '''
        Here we need to get the diference between closing prices of the day and the previous day
        '''
        for i in range(len(close) -1):
            variation.append(float(close[i]) - float(close[i + 1]))
        
        variation.pop(0)
        variation.insert((len(variation)), 0)

        return variation
    get_varation(close)



    def info_json(open_price, high_price, low_price, close , variation):
        '''
        This is the first step to convert the list into a json file
        We need a dictionary to store the information
        '''
        json_data['open_price'] = open_price
        json_data['high_price'] = high_price
        json_data['low_price'] = low_price
        json_data['close'] = close
        json_data['variation'] = variation
        return json_data
    info_json(open_price, high_price, low_price, close , variation)
    
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
                'close': close[i],
                'variation' : variation[i],
            })
    create_json()

    info = {
        simbol : data
    }
    return JsonResponse(info)



