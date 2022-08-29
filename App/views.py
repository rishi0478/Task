from base64 import decode
from urllib import request
from django.contrib import messages
from App.models import Profile,student_db
from django.shortcuts import render,redirect
from rest_framework import status
from rest_framework.decorators import api_view,APIView
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
from App.serializer import Login_user,Student_serializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import OutstandingToken

# -------------------   Api Authenticaion -------------

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import jwt
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

@api_view(['POST'])
def serializer_login(request):
    if request.method == 'POST':
        serializer = Login_user(data = request.data)
        print(serializer)
        if serializer.is_valid():
            username = serializer.data.get('username')
            print(username)
            password = serializer.data.get('password')

            user_obj = User.objects.get(username = username)
            profile_bojjj = Profile.objects.filter(user = user_obj).first()

            if not profile_bojjj.is_active:
                return Response({'msg':"Profile is not verified Check your email"},status=status.HTTP_204_NO_CONTENT)


            global user_name_temp
            user_name_temp = username

            user = authenticate(username = username, password = password)
            if user is not None:
                return Response({'msg':'Login success'},status=status.HTTP_200_OK)
            else:
                return Response({'error':'Invalid Username password'},status=status.HTTP_502_BAD_GATEWAY)


class func(APIView):
    authentication_classes = [ JWTAuthentication ]
    permission_classes = [ IsAuthenticated ]

    def get(self,request):
        raw_data = student_db.objects.all()
        serializer = Student_serializer(raw_data,many=True)
        # token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        # data = {'token': token}
        # print(data)
        # print(request.user.username)
        # print(jwt.decode(token,'',algorithm=['HS256']))
        return Response(serializer.data)

    def post(self,request):
        serializer = Student_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            stu_obj = serializer.data.get('name')
            raw_id = student_db.objects.filter(name__exact=stu_obj).values('id')
            filter_key = raw_id[0]['id']
            var = student_db.objects.get(id = filter_key)
            hold_username = request.user.username
            var.created_by = hold_username
            var.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class token_exp(APIView):
    def post(self,request):
        # print(request.user.auth_token,"here")
        # logout(request)
        # breakpoint()
        # acess_token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        refresh_token = RefreshToken(request.data.get('refresh'))
        print(refresh_token,"--------->")
        OutstandingToken.objects.filter(token=refresh_token).delete()
        # print(dd)

        return Response("f")
        # try:
        #     tokens = RefreshToken(request.data.get('refresh'))
        #     print(tokens)
        #     print(request.user.username,"------")
        #     tokens.blacklist()
            
        #     return Response({"Token is expired"},status=status.HTTP_200_OK)
        
        # except Exception as e:
        #     print(str(e))
        #     return Response(status=status.HTTP_400_BAD_REQUEST)


















    



