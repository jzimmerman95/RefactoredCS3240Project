from django.shortcuts import render

# Create your views here.
def view_form(request):
        return render(request, 'formtest/form.html', {})
