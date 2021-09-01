from django.urls import path
from .views import customer_fave_sellers

urlpatterns = [
    path('reports/customer_favorite_sellers', customer_fave_sellers),
]
