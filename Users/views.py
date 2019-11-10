from django.shortcuts import render,redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout

# Create your views here.

def signinpage(request):
    logform = LoginForm(None)
    regform = RegisterForm(request.POST or None) 

    if regform.is_valid():
        #Getting values
        username = regform.cleaned_data.get("username")
        password = regform.cleaned_data.get("password")
        email = regform.cleaned_data.get("email")
        #Creating New User
        newuser = User(username= username, email = email)
        newuser.set_password(password)
        newuser.save()
        user = authenticate(username=username, password=password)
        login(request,user)
        return redirect("Index")

    try:
        message = request.session["loginerror"]
        request.session["loginerror"] = None
    except:
        message = None
    finally:
        context = {
            "regform":regform,
            "logform":logform,
            "message":message,

        }
        return render(request,"signin.html",context)

def userlogin(request):
    logform = LoginForm(request.POST)

    if logform.is_valid():
        #Getting values
        rusername = logform.cleaned_data.get("rusername")
        rpassword = logform.cleaned_data.get("rpassword")

        #Login Try
        user = authenticate(username=rusername, password=rpassword)
        if user is None:
            request.session["loginerror"] = "Invalid Username or Password"
            return redirect("SignIn")
        #Login Success
        if logform.cleaned_data.get("rememberme"):
            request.session.set_expiry(1209600)#2 weeks

        login(request,user)
    return redirect("Index")

def signout(request):
    logout(request)
    return redirect("Index")