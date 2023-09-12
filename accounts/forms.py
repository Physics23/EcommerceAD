from django import forms
from accounts.models import Account, UserProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'enter password', 'class':'form-control'}))
    conf_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'confirm password', 'class':'form-control'}))
    class Meta:
        model = Account
        fields = ['first_name','last_name','phonnumber', 'email','password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']= 'enter first_name'
        self.fields['last_name'].widget.attrs['placeholder']= 'enter last_name'
        self.fields['email'].widget.attrs['placeholder']= 'enter email adress'
        self.fields['phonnumber'].widget.attrs['placeholder']= 'enter phonnumber'
        for field in self.fields:
            self.fields[field].widget.attrs['class']= 'form-control'


  #password validation

    def clean(self):
       cleaned_data = super(RegistrationForm, self).clean()
       password = cleaned_data.get('password')
       conf_password = cleaned_data.get('conf_password')

       if password != conf_password:
           raise forms.ValidationError('password missmach')


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name','phonnumber')
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']= 'form-control'




class UserProfileForm(forms.ModelForm):
    profilepicture = forms.ImageField(required=False, error_messages={'invalid':('image field only')}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields =('adress_line1', 'adress_lin2', 'state','city','country', 'profilepicture')
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']= 'form-control'

# contact class
class ContacForm(forms.Form):
     subject = forms.CharField(max_length=100)
     message = forms.CharField(widget=forms.Textarea)
     sender = forms.EmailField()
