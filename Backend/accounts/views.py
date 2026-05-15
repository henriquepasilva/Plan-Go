from django.shortcuts import render

# Create your views here.
def login_view(request):
    return render(request, 'accounts/login.html')

def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')