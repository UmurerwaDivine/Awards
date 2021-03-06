# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from . form import ProfileUploadForm,ProfileForm,ImageForm
from django.http  import HttpResponse
from . models import Pic,Profile
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import MerchSerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly

# Create your views here.
# @login_required(login_url='/accounts/login/')
def index(request):
      title = 'Awards'
      pic_posts = Pic.objects.all()
      # comments = Comment.objects.all()

    #   print(pic_posts)
      return render(request,'index.html',{"title":title,"pic_posts":pic_posts})
def search_results(request):
    if 'pic_name' in request.GET and request.GET["pic_name"]:
        search_term = request.GET.get("pic_name")
        searched_profiles = Pic.search_pic(search_term)
        message = f"{search_term}"

        return render(request, 'search_pic.html',{"message":message,"pics": searched_profiles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search_pic.html',{"message":message})

@login_required(login_url='/accounts/login/')
def profile(request):
	 current_user = request.user
	 profile = Profile.objects.all()
	

	 return render(request, 'profile.html',{"current_user":current_user,"profile":profile})
@login_required(login_url='/accounts/login/')
def upload_profile(request):
    current_user = request.user 
    title = 'Upload Profile'
    try:
        requested_profile = Profile.objects.get(user_id = current_user.id)
        if request.method == 'POST':
            form = ProfileUploadForm(request.POST,request.FILES)

            if form.is_valid():
                requested_profile.profile_pic = form.cleaned_data['profile_pic']
                requested_profile.bio = form.cleaned_data['bio']
                requested_profile.username = form.cleaned_data['username']
                requested_profile.save_profile()
                return redirect( 'profile' )
        else:
            form = ProfileUploadForm()
    except:
        if request.method == 'POST':
            form = ProfileUploadForm(request.POST,request.FILES)

            if form.is_valid():
                new_profile = Profile(profile_pic = form.cleaned_data['profile_pic'],bio = form.cleaned_data['bio'],username = form.cleaned_data['username'])
                new_profile.save_profile()
                return redirect( 'profile' )
        else:
            form = ProfileUploadForm()


    return render(request,'upload_profile.html',{"title":title,"current_user":current_user,"form":form})
@login_required(login_url='/accounts/login/')
def send(request):
    '''
    View function that displays a forms that allows users to upload images
    '''
    current_user = request.user

    if request.method == 'POST':

        form = ImageForm(request.POST ,request.FILES)

        if form.is_valid():
            image = form.save(commit = False)
            image.user_key = current_user
            image.save() 

            return redirect('index')
    else:
        form = ImageForm() 
    return render(request, 'send.html',{"form" : form}) 
class MerchList(APIView):
    def get(self, request, format=None):
        permission_classes = (IsAdminOrReadOnly,)
        all_merch = Pic.objects.all()
        serializers = MerchSerializer(all_merch, many=True)
        return Response(serializers.data)
    def post(self, request, format=None):
        serializers = MerchSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Create your views here.
