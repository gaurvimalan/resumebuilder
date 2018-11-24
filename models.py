from django.db import models
import json
from rest_framework import status
from django.conf import settings
from django.http import HttpResponse
from rest_framework.response import Response
from resume_builder.tasks import resume_download_under_process

# Create your models here.
class Candidate(models.Model):
	name = models.CharField(blank=False, max_length=70) 
	email = models.EmailField(blank=False, max_length=50)
	phone = models.CharField(blank=False, max_length=15)
	address = models.CharField(blank=False, max_length=70)
	website = models.CharField(blank=True, max_length=40)
	dob = models.DateField(blank=True, max_length=20)

class Experience(models.Model):
	careerObjective = models.CharField(blank=False, max_length=250)
	totalExperience = models.DateField(blank=True, max_length=40)


class Profile(models.Model):
	profile = models.CharField(blank=True, max_length=100)
	username = models.CharField(blank=True, max_length=50)
	url = models.URLField(blank=True, max_length=200)

class Work(models.Model):
	company = models.CharField(blank=True, max_length=70)
	position = models.CharField(blank=True, max_length=40)
	location = models.CharField(blank=True, max_length=35)
	website = models.CharField(blank=True, max_length=35)
	startDate = models.DateField(blank=True, max_length=12)
	endDate = models.DateField(blank=True, max_length=12)
	summary = models.CharField(blank=True, max_length=300)

class Project(models.Model):
	name = models.CharField(blank=True, max_length=35)
	url = models.URLField(blank=True, max_length=40)
	startDate = models.DateField(blank=True, max_length=12)
	endDate = models.DateField(blank=True, max_length=12)
	summary = models.CharField(blank=True, max_length=300)

class Skill(models.Model):
	languages = models.CharField(blank=True, max_length=150)
	Tools = models.CharField(blank=True, max_length=150)
	Platforms = models.CharField(blank=True, max_length=150)
	Services = models.CharField(blank=True, max_length=150)

class Education(models.Model):
	institution = models.CharField(blank=False, max_length=70)
	area = models.CharField(blank=False, max_length=35)
	location = models.CharField(blank=False, max_length=35)
	branch = models.CharField(blank=False, max_length=35)
	studyType = models.CharField(blank=False, max_length=35)
	startDate = models.CharField(blank=False, max_length=12)
	endDate = models.CharField(blank=False, max_length=12)
	gpa = models.FloatField(blank=False, max_length=20)

class Award(models.Model):
	title = models.CharField(blank=True, max_length=35)
	date = models.DateField(blank=True, max_length=12)
	awarder = models.CharField(blank=True, max_length=70)
	summary = models.CharField(blank=True, max_length=300)


class Language(models.Model):
	languages = models.CharField(blank=True, max_length=35)


class Interest(models.Model):
	title = models.CharField(blank=True, max_length=35)


class CandidateProfile(models.Model):
	basics = models.OneToOneField(Candidate)
	experience = models.OneToOneField(Experience)
	profiles = models.ManyToManyField(Profile)
	work = models.ManyToManyField(Work)
	projects = models.ManyToManyField(Project)
	skills = models.ManyToManyField(Skill)
	education = models.ManyToManyField(Education)
	awards = models.ManyToManyField(Award)
	languages = models.ManyToManyField(Language)
	interests = models.ManyToManyField(Interest)
	urls = models.CharField(blank=True, max_length=2000)
	save_pdf = True

	






	def mandatory_fields(self,flag=True):
		# import ipdb; ipdb.set_trace();
		fields = ['basics','experience','projects','skills','education','awards','languages','interests']
		
		for f in fields:
			if not getattr(self,f):
				flag=False
				break
			else:
				flag=True
		return flag
	



	def save(self, *args, **kwargs):
		# import ipdb; ipdb.set_trace();
		if self.id:
			objt_id = self.id
			obj_id = json.dumps(objt_id)
			obj = CandidateProfile.objects.get(id=self.id)
			if self.mandatory_fields() and self.save_pdf:
				resume_download_under_process.delay(obj_id)
				# return Response(
    #                     {"status": 1, "msg": 'order is under progress'},
    #                     status=status.HTTP_200_OK)
		super(CandidateProfile, self).save(*args, **kwargs)
		

		# if not self.basics:
		# 	return False
		# if not self.experience:
		# 	return False
		# if not self.projects:
		# 	return False
		# if not self.skills:
		# 	return False
		# if not self.education:
		# 	return False
		# if not self.awards:
		# 	return False
		# if not self.languages:
		# 	return False
		# if not self.interests:
		# 	return False
			
		

					# fname = f.name
   #      	get_choice = 'get_'+fname+ 
   #      	if hasattr(self, get_choice):
   #          	value = getattr(self, get_choice)()
			# 	if value:
			# 		return True
			# 	else:
			# 		return False


