from django import forms
from .models import Utilisateur

class UtilisateurForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenom', 'email', 'role', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user