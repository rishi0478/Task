from django.contrib import messages
from App.models import Profile
from django.shortcuts import render,redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from App.serializer import User_serializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
import uuid
from django.contrib.auth.decorators import login_required
from App.utlis import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse 
# Create your views here.

@api_view(['GET','POST'])
def auth_system_func(request):
    if request.method == 'GET':
        User_data = User.objects.all()
        serializer = User_serializer(User_data,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        print(data)

        if User.objects.filter(email = data['email']).first():
            return Response('Email is Taken',status=status.HTTP_400_BAD_REQUEST)


        serializer = User_serializer(data= data)
        print(serializer,'-------- imp ---------')
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data

            # Profile detail save --------------
            user_obj = User.objects.get(username = data['username'])
            my_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj , auth_token = my_token)
            profile_obj.save()
            print('here we go --- ')

            # Eamil Part -------
            user= User.objects.get(email=data['email' ])
            print(user,'------555-------')
            current_site = get_current_site(request).domain
            # relativeLink = reverse('/Verify/')
            
            
            link_ab = 'http://'+ current_site + '/Verify/' + my_token
            email_body = "Hi "+data['username']+" use link below to verify the email \n"+link_ab

            raw_data = {'email_body': email_body , 'email_subject':' verify your email ', 'to_email':data['email'] }
            Util.send_mail(raw_data)
             
            
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)



def Verify_email(request,auth_token):
    try:
        profile_objj= Profile.objects.filter(auth_token = auth_token).first()
        if profile_objj:
            # ------
            if profile_objj.is_active == True:
                messages.success(request,'your Account is already verified sir')
                return redirect('login')
                # ------
            profile_objj.is_active = True
            profile_objj.save()
            messages.success(request,'Your account has been verified')
            return redirect('login')
    except Exception as e:
        print(e)

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        print(username)
        password = request.POST['password']
        print(password)

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request,'User not found')
            return redirect('login')

        profile_bojjj = Profile.objects.filter(user = user_obj).first()

        if not profile_bojjj.is_active:
            messages.success(request,'Profile is not verified Check your email')
            return redirect ('login')
        user = authenticate(username = username , password = password)
        print(user)
        if user is not None:
            
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Incorrect Username and password')
            return redirect('login')

    else:
        return render(request,'index.html')


@login_required(login_url='login')
def home_page(request):
    if request.method == 'GET':
        return render(request,'home.html')


def logout_session(request):
    logout(request)
    return redirect('login')


    



