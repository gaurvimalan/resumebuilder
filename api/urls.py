from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^downloadresume/$', views.DownloadResumeAPIView.as_view(), name="download-resume"),
    url(r'^(?P<order_id>[0-9]+)/$',views.ResumePreviewView.as_view(), name="format-resume"),
    url(r'^selectresume/$', views.SelectResumeView.as_view(), name="select-resume"),


]
