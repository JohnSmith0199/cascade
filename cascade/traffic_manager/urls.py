from django.urls import path

from . import views, api

urlpatterns = [
    path('validate/', api.validate_token),
    path('clean/', api.clean_tokens),
    path('', views.index),
    path('<str:campaign_id>/', views.index, name='index'),
]
