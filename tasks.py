# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


# Create your views here.
import subprocess
import os
import json
import time
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings
# from celery.contrib import rdb
from rest_framework.views import APIView
from celery.decorators import task


@task(name="resume_download_under_process")
def resume_download_under_process(obj_id):
    # rdb.set_trace();
    # import ipdb; ipdb.set_trace();
    from resume_builder.models import CandidateProfile
    obj = CandidateProfile.objects.get(id=obj_id)
    latex_file_type = {
        'pdflatex': [1, 3, 4, 5],
        'xelatex': [2]
    }
    
    

    # create_timestamp=str(int(time.time()))
    # mydata = request.data.copy()
    # print(mydata)
    # serializer = ResumeSerializer(data=mydata)
    # if serializer.is_valid(raise_exception=False):
    one_to_one_fields = ['basics','experience']
    many_to_many_fields = ['profiles','work','projects','skills','education','awards','languages','interests']

    mydata = {}
    urls = []
    for i in one_to_one_fields:
        mydata[i] = getattr(obj,i).__dict__

    for i in many_to_many_fields:
        mydata[i] = []
        for sobj in getattr(obj,i).all():
            mydata[i].append(sobj.__dict__)
    extra_data = {"userid":113413}
    a = mydata
    mydata = a.copy()
    mydata.update(extra_data)
    
    # for i in templateid:
    #     mydata.update(templateid)
    # print (mydata)
    # mydata = mydata+mydata
    # templateid_list = ['1','2','3','4','5']
    templateid_list = ['3','4']
    for templateid in templateid_list:
        if mydata:
            create_timestamp=str(int(time.time()))
        
            # templateid = mydata['templateid']
            rendered = render_to_string(os.path.join(templateid, "jinja.tex"),
                                        {'resumeData': mydata})
            input_file_path = os.path.join(
                settings.MEDIA_ROOT,
                "templates",
                templateid,
                templateid + ".tex")
            with open(input_file_path, "wb+") as file:
                file.write(rendered.encode("utf-8"))

            outputdir = os.path.join(
                settings.MEDIA_ROOT, "resumes","%(userid)s_%(usetimestamp)s" % {"usetimestamp": create_timestamp, "userid": mydata['userid']} )
            os.mkdir(outputdir)
            changedir = os.path.dirname(input_file_path)

            command = 'pdflatex' if templateid in latex_file_type['pdflatex'] else 'xelatex'
            command_args = "cd %(changedir)s;%(command)s -interaction=nonstopmode -output-directory=%(outputdir)s %(input_file_path)s" % {
                'command': command, "changedir": changedir, 'outputdir': outputdir,
                'input_file_path': input_file_path}
            proc = subprocess.Popen(
                command_args,
                stderr=subprocess.PIPE,
                shell=True,
                stdout=subprocess.PIPE,
                stdin=subprocess.PIPE)
            proc.wait()
            # import ipdb; ipdb.set_trace();
            

            
            with open(os.path.join(settings.MEDIA_ROOT, "resumes",
                                   "%(userid)s_%(usetimestamp)s" % {"usetimestamp": create_timestamp, "userid": mydata['userid']}, templateid +
                                   ".pdf"), 'rb') as pdffile:
                pdf_contents = pdffile.read()
                new_url = "resumes/{userid}_{usetimestamp}/{filename}".format(usetimestamp=create_timestamp, userid=mydata['userid'], filename=templateid +
                                   ".pdf")
                urls.append(new_url)
    urls = str(urls)
    obj.urls = urls
    obj.save_pdf = False
    obj.save()
    # print(obj)



            # new_url = eval(obj.urls)
            # urls = urls.append(new_url)
            # urls = json.dump(urls)
            # obj.save_pdf=False
            # obj.save()



        # response = HttpResponse(
        #     pdf_contents, content_type='application/pdf')
        # response['Content-Disposition'] = 'attachment; filename="myresume.pdf"'

    # return response



