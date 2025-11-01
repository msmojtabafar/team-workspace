from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            from django.shortcuts import redirect
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

def home_redirect(request):
    if request.user.is_authenticated:
        from django.shortcuts import redirect
        return redirect('dashboard')
    else:
        from django.shortcuts import redirect
        return redirect('login')
