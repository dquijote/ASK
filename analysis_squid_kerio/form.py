from django import forms
from .models import BlackListDomain, CategoryBlackListDomain


class filter_userForm(forms.Form):
    user_cell = forms.CharField(label='User o cell', max_length=100)
    date_start = forms.DateField(label='Inicio')
    date_end = forms.DateField(label='Fin')


class FilterIncidenceForm(forms.Form):
    StarIncidence = forms.DateField(label='Fecha Inicial')
    EndIncidence = forms.DateField(label='Fecha Final')
    category = forms.ModelChoiceField(queryset=CategoryBlackListDomain.objects.all(), empty_label="Categoria")
