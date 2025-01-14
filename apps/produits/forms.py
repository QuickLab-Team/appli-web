from django import forms

from apps.produits.models import Stockage
    
class StockageForm(forms.ModelForm):
    class Meta:
        model = Stockage
        fields = ['nom', 'service']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service'].empty_label = "Aucun service"