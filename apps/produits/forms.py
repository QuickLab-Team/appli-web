from django import forms

class FileImportForm(forms.Form):
    fichier = forms.FileField()