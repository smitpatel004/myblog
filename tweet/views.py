from urllib import request

from django.shortcuts import render
from django.shortcuts import  get_object_or_404,redirect
from .models import tweet
from .forms import Tweetforms,UserRegisterationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.

def home(request):
    return render(request,'index.html')

def tweet_list(request):
    tweet1=tweet.objects.all().order_by('-created_at')
    return render(request,"tweet_list.html",{'tweet1':tweet1})

@login_required()
def tweet_create(request):
    if request.method =="POST":
        form=Tweetforms(request.POST,request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = Tweetforms()
    return render(request,'tweet_from.html',{'form':form})
@login_required()
def tweet_edit(requset,tweet_id):
    tweet12=get_object_or_404(tweet,pk=tweet_id,user=request.user)
    if request.method == "POST":
        form = Tweetforms(request.POST, request.FILES,instance=tweet12)
        if form.is_valid():
            tweet12 = form.save(commit=False)
            tweet12.user = request.user
            tweet12.save()
            return redirect('tweet_list')
    else:
        form = Tweetforms(instance=tweet12)
    return render(request, 'tweet_from.html', {'form': form})

@login_required()
def tweet_delete(request,tweet_id):
    tweet18=get_object_or_404(tweet,pk=tweet_id,user=request.user)
    if request.method == 'POST':
        tweet18.delete()
        return redirect('tweet_list')

    return render(request, 'tweet_confirm_delete.html', {'tweet18': tweet18})

def register(request):
    if request.method=="POST":
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('tweet_list')


    else:
        form=UserRegisterationForm()

    return render(request, 'registration/register.html', {'form': form})

