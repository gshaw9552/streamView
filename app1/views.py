from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
from django.conf import settings
from isodate import parse_duration
import datetime

def calculate_upload_duration(publish_time):
    publish_datetime = datetime.datetime.strptime(publish_time, "%Y-%m-%dT%H:%M:%SZ")
    current_datetime = datetime.datetime.utcnow()
    duration = current_datetime - publish_datetime
    if duration.days > 365:
        years = duration.days // 365
        if years == 1:
            return "1 year ago"
        else:
            return f"{years} years ago"
    elif duration.days > 30:
        months = duration.days // 30
        if months == 1:
            return "1 month ago"
        else:
            return f"{months} months ago"
    elif duration.days > 0:
        if duration.days == 1:
            return "1 day ago"
        else:
            return f"{duration.days} days ago"
    elif duration.seconds // 3600 > 0:
        hours = duration.seconds // 3600
        if hours == 1:
            return "1 hour ago"
        else:
            return f"{hours} hours ago"
    else:
        minutes = duration.seconds // 60
        if minutes <= 1:
            return "just now"
        else:
            return f"{minutes} minutes ago"

# Create your views here.


def homePage(request):
    return render(request, 'home.html')

def youtubeHomePage(request):
    videos = []
    channels = []

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        channel_url = 'https://www.googleapis.com/youtube/v3/channels'


        search_params = {
            'part' : 'snippet',
            'q' : request.POST['search'],
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'maxResults' : 12,
            'type' : 'video'
        }

        r = requests.get(search_url, params=search_params)
        # print(r.text)
        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        video_params = {
            'part' : 'snippet, contentDetails',
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'id' : ','.join(video_ids),
            'maxResults' : 12
        }
        

        r = requests.get(video_url, params=video_params)
        # print(r.text)
        results = r.json()['items']

        channel_ids = []
        for result in results:
            video_data = {
                'title' : result['snippet']['title'],
                'id' : result['id'],
                'url' : f'https://www.youtube.com/watch?v={ result["id"] }',
                'duration' : parse_duration(result['contentDetails']['duration']),
                'thumbnail' : result['snippet']['thumbnails']['high']['url'],
                'channelName' : result['snippet']['channelTitle'],
                'uploadTime' : calculate_upload_duration(result['snippet']['publishedAt'])
            }
            
            videos.append(video_data)
            # print(video_data['title'],'  : ',video_data['id'])
            channel_ids.append(result['snippet']['channelId'])

        channel_params = {
            'part' : 'snippet, contentDetails',
            'key' : settings.YOUTUBE_DATA_API_KEY,
            'id' : ','.join(channel_ids),
            'maxResults' : 12
        }

        r = requests.get(channel_url, params=channel_params)
        # print(r.text)
        result = (r.json()['items'])
        print(result)
        for result in results:
            channel_data = {
                'channelPfp' : result['snippet']['thumbnails']['high']['url']
            }
            print(result['snippet']['thumbnails'])

            channels.append(channel_data)

    context = {
        'videos' : videos,
        'channels' : channels
    }

    return render(request, 'youtube.html', context)

def signUpPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Exists')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Used')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Passwords mismatch')
            return redirect('signup')
    else:
        return render(request, 'signup.html')

def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Credentials invalid')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logoutPage(request):
    auth.logout(request)
    return redirect('login')

def post(request, pk):
    return render(request, 'post.html', {'pk': pk})