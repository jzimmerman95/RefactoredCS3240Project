from django.shortcuts import render

# Create your views here.
def sign_up(request):
        return render(request, 'myapplication/signIn.html', {})
