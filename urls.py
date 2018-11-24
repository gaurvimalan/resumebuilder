from django.conf.urls import include, url
from django.contrib import admin
from . views import CandidateInformationView



urlpatterns = [
    # url(r'^$',views.search_form, name='search_form'),
    url(r'^$',CandidateInformationView.as_view(), name='search_form'),
    url(r'^api/',include('resume_builder.api.urls', namespace='api')),
    # url(r'^preview/',PreviewPageView.as_view(), name='preview_page'),

]
