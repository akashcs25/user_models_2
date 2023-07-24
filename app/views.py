from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.


def registration(request):
    usfo=UserForm()
    pfo=ProfileForm()
    d={'usfo':usfo,'pfo':pfo}
    if request.method=='POST' and request.FILES:
        usfod=UserForm(request.POST)
        pfod=ProfileForm(request.POST,request.FILES)
        if usfod.is_valid() and pfod.is_valid():
            nsufo=usfod.save(commit=False)
            sub_password=usfod.cleaned_data['password']
            nsufo.set_password(sub_password)
            nsufo.save()
            nspfo=pfod.save(commit=False)
            nspfo.username=nsufo
            nspfo.save()

            send_mail('registration',
            'registration done successfully',
            'akashshivaram26@gmail.com',
            [nsufo.email],
            fail_silently=True
                )

            return HttpResponse('registration successfull')
    return render(request,'registration.html',d)


def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)

    return render(request,'home.html')


def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        if AUO:
            if AUO.is_active:
                login(request,AUO)
                request.session['username']=username
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('user is not active')
        else:
            return HttpResponse('invalid details')

    return render(request,'user_login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def display(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'display.html',d)



@login_required
def change_password(request):
    if request.method=='POST':
        PW=request.POST.get('pw')
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        
        UO.set_password(PW)
        UO.save()
        return HttpResponse('password changed successfully!!!')

    return render(request,'change_password.html')

def reset_password(request):
    if request.method=='POST':
        user=request.POST['username']
        UO=User.objects.get(username=user)
        RP=request.POST['password']
        UO.set_password(RP)
        UO.save()
        return HttpResponse('reset_password successful!!!')
    return render(request,'reset_password.html')




















