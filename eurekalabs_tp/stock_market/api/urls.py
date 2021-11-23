from django.urls import path
from stock_market.api.api_views import *

urlpatterns = [
    # User APIs:
    path('user/login/', LoginUserAPIView.as_view()),
    path('stock_information/', stock_information),
]