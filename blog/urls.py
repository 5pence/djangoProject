from django.urls import path
from . import views

# This app_name allows us to organise URLs by application and use the name when referring to them.
app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>', views.post_detail, name='post_detail'),
]
