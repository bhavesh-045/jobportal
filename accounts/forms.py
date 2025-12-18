from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
import uuid

class StudentSignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email','full_name','phone','profile_image','resume','password1','password2']

    def save(self,commit=True):
            user = super().save(commit=False)
            base_username = user.email.split('@')[0]
            user.username = f"{base_username}_{uuid.uuid4().hex[:4]}"
            user.role = 'student'
            if commit:
                user.save()
            return user
        

class RecruiterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email','full_name','phone','profile_image','password1','password2']   
        exclude = ['resume']     

    def save(self,commit=True):
            user = super().save(commit=False)
            base_username = user.email.split('@')[0]
            user.username = f"{base_username}_{uuid.uuid4().hex[:4]}"
            user.role = 'recruiter'
            if commit:
                user.save()
            return user  
    

class ProfileEditForm(forms.ModelForm):
    class Meta :
        model = CustomUser
        fields = ['full_name','phone','profile_image','resume']


    def  __init__(self, *args, **kwargs):
         user = kwargs.pop('user',None)
         super(ProfileEditForm,self).__init__(*args,**kwargs)
         if user and user.role != 'student' :
              self.fields.pop('resume')