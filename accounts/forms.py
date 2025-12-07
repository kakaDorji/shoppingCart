from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter password'
    }))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'confirmed password'
    }))
    class Meta:
        model=Account
        fields=['first_name','last_name','phone_number','email','password']

        #over write the form..customize form field..over write the form fields
    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        # taking specific fields
        self.fields['first_name'].widget.attrs['placeholder']='enter first name'
        self.fields['last_name'].widget.attrs['placeholder']='enter last name'
        self.fields['email'].widget.attrs['placeholder']='enter your email'
        self.fields['phone_number'].widget.attrs['placeholder']='enter your phone number'
       
        # it will loop through all field and assing form-control class
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
           
    # comparing password
    def clean(self):
        cleaned_data=super(RegistrationForm,self).clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(
                "password does not match!"
            )

        
