from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView



# def search_form(request):
#     return render(request, 'user_data.html')

class CandidateInformationView(TemplateView):

	def get_template_names(self):
		return ['user_data.html']

# class PreviewPageView(DetailView):

# 	def get(self, request, *args, **kwargs):
# 		return HttpResponse('done')












    