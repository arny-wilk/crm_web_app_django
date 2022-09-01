from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from crm_app.forms import UserRegistrationForm


def home(request):
    return HttpResponse("Acceuil du site")


def signup(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("app-index")
    else:
        form = UserRegistrationForm()

    return render(request, "crm_app/signup.html", {"form": form})
