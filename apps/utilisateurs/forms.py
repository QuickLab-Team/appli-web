from django import forms
from .models import Utilisateur

class UtilisateurForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenom', 'email', 'role', 'annee', 'groupe', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            if user.role == 'preparateur':
                self.fields['role'].choices = [('etudiant', 'Étudiant')]
            elif user.role == 'administrateur':
                self.fields['role'].choices = [('etudiant', 'Étudiant'), ('preparateur', 'Préparateur')]

        self.fields['annee'].required = False
        self.fields['groupe'].required = False

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')

        if role == 'etudiant':
            if not cleaned_data.get('annee'):
                self.add_error('annee', 'L\'année est requise pour un étudiant.')
            if not cleaned_data.get('groupe'):
                self.add_error('groupe', 'Le groupe est requis pour un étudiant.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
