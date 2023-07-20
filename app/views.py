from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse
from django.core.mail import send_mail
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