from django.urls import path
from stock_market.api.api_views import *

urlpatterns = [
    path('signup/', signup),
    path('stock_information/', stock_information),
]