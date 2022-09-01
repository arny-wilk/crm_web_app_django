from django import forms

JOBS = (
    ("personnel1", "Hôte d'accueil"),
    ("personnel2", "Responsable Rayon"),
    ("personnel3", "Manager")
)


class SignupForm(forms.Form):
    pseudo = forms.CharField(max_length=10, required=False)
    email = forms.EmailField()
    password = forms.CharField(min_length=6)
    job = forms.ChoiceField(choices=JOBS)
    cgu_accept = forms.BooleanField(initial=True)
