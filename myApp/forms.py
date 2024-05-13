from django import forms
from .models import User, UserFile, Feature, FeatureValidation

#
# class UserFileForm(forms.Form):
#     email = forms.EmailField()

#     file = forms.FileField(label='Upload Excel File', help_text='Only .xlsx format is allowed.')
# from django import forms
# from .models import Feature

# class UserFileForm(forms.ModelForm):
#     class Meta:
#         model = Feature
#         fields = ['email', 'user_file']
#
#     email = forms.EmailField(label='Email')
#     user_file = forms.FileField(label='User File')
# class UserFileForm(forms.Form):
#     email = forms.EmailField(label='Email')


from django import forms
from .models import User


class UserFileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
