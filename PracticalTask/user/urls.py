from django.urls import path
from .views import  *

urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('verify_login/',LoginView.as_view(),name='verify_login'),
    path('admin_index/',AdminView.as_view(),name='admin_index'),
    path('home/<int:pk>',home,name='user_index'),
    path('create_user/',CreateUserView.as_view(),name='create_user'),
    path('activate_account/<uidb64>/<token>/',activate_account, name='activate_account'),
    path('list_user/',ListUserView,name='list_user'),
    path('delete_user/<int:pk>/',DeleteUserView,name='delete_user'),
    path('update_user/<int:pk>/',UpdateUserView,name='update_user')
]