from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, logout
from django.core.mail import send_mail
from django.contrib import messages
from mypro import settings

# Create your views here.
def home(request):
    return render(request,"myapp/index.html")
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "galatbat")
            return redirect('home')
        if User.objects.filter(email=email):
            messages.error(request,"bahut galat bat")  
            return redirect('home')  

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request,  "congratulations your's account created")
        
        subject = "welcome to certificate "
        message = "hello" + myuser.first_name + "!! \n" "welcome to certificate woeld \n we have also sent mail to your registerd mail"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        return redirect('signin')

    return render(request, "myapp/signup.html")    
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "myapp/index.html", {'fname': fname})
        else:
            messages.error(request, "Bad credentials")
            return redirect('home')    
    return render(request, "myapp/signin.html")
def signout(request):
    logout(request)
    messages.success(request, "logger Out successfully")
    return redirect('home')
    pass       
