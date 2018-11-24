from rest_framework import serializers
from resume_builder.models import Candidate, Experience, Profile, Work, Project, Skill, Education, Award, Language, Interest, CandidateProfile



class basicsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Candidate
        exclude = ('address',)

class experienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Experience
        fields = '__all__'


class profilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        exclude = ('url',)


class workSerializer(serializers.ModelSerializer):

    class Meta:
        model = Work
        fields = '__all__'


class projectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        exclude = ('url',)


class skillsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = '__all__'


class educationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Education
        fields = '__all__'


class awardsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Award
        fields = '__all__'


class languagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Language
        fields = '__all__'


class interestsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interest
        fields = '__all__'


# class candidateprofileSerializer(serializers.ModelSerializer):



        


class ResumeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CandidateProfile
        fields = '__all__'



    basics = basicsSerializer()
    experience = experienceSerializer()
    profiles = profilesSerializer(many=True)
    work = workSerializer(many=True)
    projects = projectsSerializer(many=True)
    skills = skillsSerializer(many=True)
    education = educationSerializer(many=True)
    awards = awardsSerializer(many=True)
    languages = languagesSerializer(many=True)
    interests = interestsSerializer(many=True)



    # def candidate_data(basics,basics_data,many=False):
    #     if not many:
    #         serializer = basicsSerializer(data=basics_data)
    #         if serializer.is_valid():
    #             obj = serializer.save()
    #         else:
    #             obj_list = []
    #             for data in basics_data:
    #                 serializer = basicsSerializer(data=data)
    #             obj_list.append()
    #             if serializer.is_valid():
    #                 list_of_obj = serializer.save()
    #             return list_of_obj

    # def create(self,validated_data):
    #     import ipdb; ipdb.set_trace();
    #     basics_data = validated_data.get('basics')
    #     candidate_data_obj = self.candidate_data(basics_data)






    def candidate_data(self,field_name, cand_basics_data, many=False):
        # import ipdb; ipdb.set_trace();
        field_name_serializer_mapping = {"basics":basicsSerializer,"experience":experienceSerializer,"profiles":profilesSerializer,"work":workSerializer,"projects":projectsSerializer,"skills":skillsSerializer,"education":educationSerializer,"awards":awardsSerializer,"languages":languagesSerializer,"interests":interestsSerializer}
        serializer_class = field_name_serializer_mapping.get(field_name)
        field_serializer = serializer_class(data=cand_basics_data)
        # import ipdb; ipdb.set_trace();
        if not many:
            if field_serializer.is_valid():
                obj = field_serializer.save()

            return obj

        else:
            obj_list = []
            for data in cand_basics_data:
                field_serializer = serializer_class(data=data)
                if field_serializer.is_valid():
                    obj = field_serializer.save()
                    obj_list.append(obj)
            return obj_list


    def create(self,validated_data):
        # import ipdb; ipdb.set_trace();
        profile = CandidateProfile()
        
        field_names = ['basics','experience','profiles','work','projects','skills','education','awards','languages','interests']
        field_dict = {'basics':False,'experience':False,'profiles':True,'work':True,'projects':True,'skills':True,'education':True,'awards':True,'languages':True,'interests':True}
        multi_value_data = {}

        for field in field_names:
            cand_basics_data = validated_data.get(field)
            is_many = field_dict.get(field)
            candidate_data_obj = self.candidate_data(field,cand_basics_data,many=is_many)
            if is_many:
                multi_value_data[field] = candidate_data_obj
            else:
                setattr(profile,field,candidate_data_obj)

        profile.save()
        # import ipdb; ipdb.set_trace();

        for key,value in multi_value_data.items():
            setattr(profile,key,value)

        profile.save()
        # import ipdb; ipdb.set_trace();
        obj = CandidateProfile.objects.filter(basics__email=validated_data['basics']['email']).order_by('-id').first()
        return obj

        # cand_experience = validated_data.get('experience')
        # cand_profiles = validated_data.get('profiles')
        # cand_work = validated_data.get('work')
        # cand_projects = validated_data.get('projects')
        # cand_skills = validated_data.get('skills')
        # cand_education = validated_data.get('education')
        # cand_awards = validated_data.get('awards')
        # cand_languages = validated_data.get('languages')
        # cand_interests = validated_data.get('interests')

        # candidate_data(basics, validated_data.get('basics'))


        # fields = ['basics','experience','profiles','work','projects','skills','education','awards','languages','interests']
        # data = ['cand_basics','cand_experience','cand_profiles','cand_work','cand_projects','cand_skills','cand_education','cand_awards','cand_languages','cand_interests']


        # def create(self, validated_data):
        #     import ipdb; ipdb.set_trace();
        #     basics_data = validated_data.pop('basics')
        #     basic = Candidate.objects.create(**validated_data)
        #     for basic_data in basics_data:
        #         CandidateProfile.objects.create(basic=basic, **basic_data)
        #     return basic


        # serializer = basicsSerializer(mydata=mydata)
        # serializer.is_valid()
        # serializer.save()



