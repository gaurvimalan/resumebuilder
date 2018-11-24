# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


# Create your views here.
import subprocess
import os
import json
import time
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponse
from rest_framework.response import Response
from django.conf import settings
from .serializers import ResumeSerializer
from resume_builder.tasks import resume_download_under_process
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from django.views.generic.base import TemplateView
from resume_builder.models import CandidateProfile
from rest_framework import status

class DownloadResumeAPIView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = None
    
    def post(self,request,*args,**kwargs):
        
        latex_file_type = {
            'pdflatex': [1, 3, 4, 5],
            'xelatex': [2]
        }
        # import ipdb; ipdb.set_trace();

        
        create_timestamp=str(int(time.time()))
        mydata = request.data.copy()
        serializer = ResumeSerializer(data=mydata)
        # import ipdb; ipdb.set_trace();
        if serializer.is_valid(raise_exception=False):
            obj = serializer.create(mydata)
            # import ipdb; ipdb.set_trace();
            
            return Response(
                        {"status": 1, "msg": 'order is under progress',"order_id":obj.pk},
                        status=status.HTTP_200_OK)
        #     resume_download_under_process.delay(mydata=mydata)
            
        #     return Response(
        #                 {"status": 1, "msg": 'order is under progress'},
        #                 status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, content_type= "application/json")


class ResumePreviewView(RetrieveAPIView):
    authentication_classes = []
    queryset = CandidateProfile.objects.all()
    permission_classes = []
    serializer_class = ResumeSerializer
    # pk_url_kwarg = 'pk'
    # slug_url_kwarg = None
    lookup_url_kwarg = 'order_id'


    # def get_object(self, queryset=None):
    #     """
    #     Returns the object the view is displaying.

    #     By default this requires `self.queryset` and a `pk` or `slug` argument
    #     in the URLconf, but subclasses can override this to return any object.
    #     """
    #     # Use a custom queryset if provided; this is required for subclasses
    #     # like DateDetailView

    #     import ipdb; ipdb.set_trace()
    #     if queryset is None:
    #         queryset = self.get_queryset()

    #     # Next, try looking up by primary key.
    #     pk = self.kwargs.get(self.pk_url_kwarg, None)
    #     slug = self.kwargs.get(self.slug_url_kwarg, None)
    #     if pk is not None:
    #         queryset = queryset.filter(pk=pk)

    #     # Next, try looking up by slug.
    #     if slug is not None and (pk is None or self.query_pk_and_slug):
    #         slug_field = self.get_slug_field()
    #         queryset = queryset.filter(**{slug_field: slug})

    #     # If none of those are defined, it's an error.
    #     if pk is None and slug is None:
    #         raise AttributeError("Generic detail view %s must be called with "
    #                              "either an object pk or a slug."
    #                              % self.__class__.__name__)

    #     try:
    #         # Get the single item from the filtered queryset
    #         obj = queryset.get()
    #     except queryset.model.DoesNotExist:
    #         raise Http404(_("No %(verbose_name)s found matching the query") %
    #                       {'verbose_name': queryset.model._meta.verbose_name})
    #     return obj

    # def get(self,request,*args,**kwargs):
    #     url = {1:"http://127.0.0.1:8000/media/resumes/113413_1539083489/3.pdf",
    #         2:"http://127.0.0.1:8000/media/resumes/113413_1539089017/3.pdf" ,
    #         3:"http://127.0.0.1:8000/media/resumes/113413_1539166753/3.pdf",
    #         4:"http://127.0.0.1:8000/media/resumes/113413_1539168782/3.pdf",
    #         5:"http://127.0.0.1:8000/media/resumes/113413_1539176200/3.pdf"}

    #     return Response({"urls":url},status=status.HTTP_200_OK)

class SelectResumeView(TemplateView):
    template_name = 'resume_builder/hello.html'

    def get_context_data(self, **kwargs):
        # import ipdb; ipdb.set_trace();
        order_id = self.request.GET.get('order_id', None)
        context = super(SelectResumeView, self).get_context_data(**kwargs)
        context.update({
                'order_id': order_id, 
            })
        return context

        
        # if order_id:


        #     r = requests.get(settings.MAIN_DOMAIN_PREFIX+ '/resume_builder/api/'+ order_id + '/')



        #     info = r.json()
            # return render()




