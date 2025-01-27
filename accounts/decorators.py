from django.http import HttpResponse
from django.shortcuts import redirect


def unautheicated_user(view_func):
    def warapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request,*args,**kwargs)
    
    return warapper_func