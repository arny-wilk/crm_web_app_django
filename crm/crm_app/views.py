from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from crm_app.forms import UserRegistrationForm


def home(request):
    return HttpResponse("Acceuil du site")


def signup(request):
    context = {}

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("app-index")
        else:
            context["errors"] = form.errors

    form = UserRegistrationForm()
    context["form"] = form

    return render(request, "crm_app/signup.html", context=context)
