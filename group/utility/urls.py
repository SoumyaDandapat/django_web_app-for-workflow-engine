from django.urls import path
from .import views

urlpatterns = [
    path('',views.registration  , name='registration'),
    path('form',views.form , name = 'form'),
    path('index' ,views.login_request, name = 'index'),
    path('get_data' ,views.get_data, name = 'get_data'),
    path('post_data' ,views.post_data, name = 'post_data'),
    path('admin' ,views.admin, name = 'admin')
]