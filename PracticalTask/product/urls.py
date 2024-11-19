from django.urls import path
from .views import  *

app_name = 'product'

urlpatterns = [
    path('create/',ProductCreateView,name="create_product"),
    path('list/',ProductListView,name="list_product"),
    path('update/<int:pk>/',ProductUpdateView,name="update_product"),
    path('delete/<int:pk>/',ProductDeleteView,name="delete_product")
]