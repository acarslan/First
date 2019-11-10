from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(
        attrs={"class" : "form-control", "aria-describedby" : "emailHelp", "placeholder" : "Email"}
    ))
    username = forms.CharField(max_length=20, min_length= 4, label = "Username",widget=forms.TextInput(
        attrs={"class" : "form-control", "placeholder" : "Username"}
    ))
    password = forms.CharField(max_length=16,min_length= 8, label = "Password", widget=forms.PasswordInput(
        attrs={"class" : "form-control", "placeholder" : "Password"}
    ))
    repassword = forms.CharField(max_length=16,min_length= 8, label = "Password Confirmation", widget=forms.PasswordInput(
        attrs={"class" : "form-control", "placeholder" : "Password Check"}
    ))
    #Validations
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        repassword = self.cleaned_data.get("repassword")
        email = self.cleaned_data.get("email")
        errorcheck = False
        errors = {}
        
        if password and repassword and password != repassword:
            errors["password"] = "Incorrect passwords"
            errorcheck = True
        
        if username and not username.isalnum():
           errors["username"] = "You can only user Alphanumeric characters for username like a2B3xyz "
           errorcheck = True
        else:
            try:
                User.objects.get(username=username)
                errorcheck = True
                errors["username"] = "\nThis username is already taken"
            finally:
                try:
                    User.objects.get(email = email)
                    errors["email"] = "This email address is alredy in use"
                except:
                    if errorcheck:
                        raise forms.ValidationError(errors)
                
                raise forms.ValidationError(errors)


        values = {
            "username" : username,
            "password" : password,
            "email" : email
        }
        return values

class LoginForm(forms.Form):
    rusername = forms.CharField(max_length=20, min_length= 4, label="Username", widget=forms.TextInput(
        attrs={"class" : "form-control", "placeholder" : "Enter Your Username"}
    ))
    rpassword = forms.CharField(max_length=16, min_length= 8,label = "Password",widget=forms.PasswordInput(
        attrs={"class" : "form-control", "placeholder" : "Password"}
    ))
    rememberme = forms.BooleanField(label = "Remember Me", required=False, widget=forms.CheckboxInput(
        attrs={"class" : "form-check-input"}
    ))
#Validations
    