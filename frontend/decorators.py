from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.views import redirect_to_login


def authorised_user(roles=[]):
    def decorator(view_func):
        def verify_func(request,*args, **kwargs):

            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group in roles:
                return view_func(request,*args, **kwargs)
            else:
                return HttpResponse('you are not authorised to view this page')

        return verify_func

    return decorator





def cart_decorator(view_func):
    def verify_func(request,*args,**kwargs):

        if request.user.is_authenticated:

            return view_func(request,*args,**kwargs)

        else:
            return redirect('login')

    return verify_func