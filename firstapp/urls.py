from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('consultation/', index, name="consultation"),
    path('courier/', courier, name="courier"),
    path('delete_courier/<int:id>', delete_courier, name="delete_courier"),
    path('products/', products, name="products"),

    path('products/delete/<int:id>', delete, name='delete'),
    path('sales/', sales, name="sales"),
    path('notes/', notes, name="notes"),
    path('signin/', signin, name="signin"),
    path('account/signup/', signup, name="signup"),

    path('orders/', orders, name="orders"),
    path('graphics/', graphics, name="graphics"),
    path('download_excel_products/', excel_products, name="download_excel_products"),
    path('download_excel_excel/', excel_sales, name="download_excel_sales"),
]
