from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from.models import Profile
from quiz.models import QuizSubmission
import json 


def register(request):
    if request.user.is_authenticated:
        return redirect('profile', request.user.username)

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
                new_profile = Profile.objects.create(user=user_model)
                new_profile.save()
                return redirect('profile', username)
        else:  
            messages.info(request, "Password not matching.")
            return redirect("register")

    context = {}
    return render(request,"register.html", context)


@login_required
def editProfile(request):

    user_object = request.user
    user_profile = request.user.profile

    if request.method == "POST":
       #Image
       if request.FILES.get('profile_img') != None:
         user_profile.profile_img = request.FILES.get('profile_img')
         user_profile.save()

       #Email
       if request.POST.get('email') != None:
           u = get_object_or_404(User, email=request.POST.get('email'))

           if u == None:
               user_object.email = request.POST.get('email')
               user_object.save()
           else:
               if u!= user_object:
                   messages.info(request,"Email Already Used, Choose a different one!")
                   return redirect('edit_profile')
               
       #Username
       if request.POST.get('username') != None:
           u = get_object_or_404(User, username=request.POST.get('username'))

           if u == None:
               user_object.username = request.POST.get('username')
               user_object.save()
           else:
               if u!= user_object:
                   messages.info(request,"Username Already Taken, Choose a unique one!")
                   return redirect('edit_profile')

       #firstname lastname         
       user_object.first_name = request.POST.get('firstname')
       user_object.last_name = request.POST.get('lastname')
       user_object.save()

       # position bio
       user_profile.position = request.POST.get('position')
       user_profile.bio = request.POST.get('bio')
       user_profile.save()

       return redirect('profile',user_object.username)
       
    context ={"user_profile":user_profile}
    return render(request, "profile-edit.html",context)

@login_required
def deleteProfile(request):

    user_object = request.user
    user_profile = request.user.profile

    if request.method == "POST" :
        user_profile.delete()
        user_object.delete()
        return redirect('logout')

    return render(request, "confirm.html")

def login(request):
    if request.user.is_authenticated:
        return redirect('profile', request.user.username)
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me') 
        
        user =auth.authenticate(username=username, password=password)

        if user is not None:
          auth.login(request, user)
          return redirect('profile',username)
        else:
            messages.info(request, 'Credential Invalid')
            return redirect('login')
        
    return render(request, "login.html")

@login_required

def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required
def profile_view(request, username):
    user_profile2 = get_object_or_404(Profile, user__username=username)
    submissions = QuizSubmission.objects.filter(user=user_profile2.user).order_by('submitted_at')

    labels = []
    scores = []

    for submission in submissions[:6]:
        labels.append(submission.quiz.title[:15])  # truncate for better chart display
        scores.append(submission.score)

    graph_data = {
        'labels': labels,
        'scores': scores,
    }

    context = {
        'user_profile2': user_profile2,
        'submissions': submissions,
        'graph_data_json': json.dumps(graph_data),
    }

    return render(request, 'profile.html', context)
