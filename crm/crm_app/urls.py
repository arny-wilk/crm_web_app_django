from django.urls import path

from crm_app.views import home, signup

urlpatterns = [
    path('', home, name="app-index"),
    path('nouveau/', signup, name="signup")
]
