from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from.models import Profile
# Create your views here.

def register(request):

    if request.method == "POST" :
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:

            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken.")
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already used, Try to login.")
                return redirect("register")
            else:
                # create user.
                user =User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # log in user and redirect to profile
                user_login =auth.authenticate(username=username, password=password)
                auth.login(request,user_login)

                # create profile for new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, email_address=email)
                new_profile.save
                return redirect('profile', username)
        else:  
            messages.info(request, "Password not matching.")
            return redirect("register")

    context = {}
    return render(request,"register.html", context)


def profile(request, username):

    user_object = User.objects.get(username=username)
    user_profile = Profile.objects.get(user=user_object)

    context = {"user_profile": user_profile}
    return render(request,"profile.html", context)

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user_login =auth.authenticate(username=username, password=password)
        auth.login(request,user_login)
    
    return render(request, "login.html")