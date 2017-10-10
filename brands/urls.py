from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.vote),
    url(r'^results$', views.results),
]
