from django import forms
from accounts.models import Account

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
