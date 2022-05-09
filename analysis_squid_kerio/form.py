import datetime

from django import forms
from .models import BlackListDomain, CategoryBlackListDomain


class filter_userForm(forms.Form):
    user_cell = forms.CharField(label='Cell', max_length=100,
                                widget=forms.TextInput(
                                    attrs={
                                        'placeholder': 'Usuario',

                                    }))
    date_start = forms.DateField(label='Inicio',
                                 widget=forms.TextInput(
                                     attrs={
                                         'placeholder': 'Fecha Inicial',

                                     }))
    date_end = forms.DateField(label='Fin',
                               widget=forms.TextInput(
                                   attrs={
                                       'placeholder': 'Fecha Final',

                                   }))
    category = forms.ModelChoiceField(queryset=CategoryBlackListDomain.objects.all(), empty_label="Categoria", label="Categoria")


class FilterIncidenceForm(forms.Form):
    StarIncidence = forms.DateField(label='Fecha Inicial',
                                    widget=forms.TextInput(
                                        attrs={
                                            'placeholder': 'Fecha Inicial',

                                        }))
    EndIncidence = forms.DateField(label='Fecha Final',
                                   widget=forms.TextInput(
                                       attrs={
                                           'placeholder': 'Fecha Final',

                                       }))
    category = forms.ModelChoiceField(queryset=CategoryBlackListDomain.objects.all(), empty_label="Categoria", label="Categoria")


class RangeDateForm(forms.Form):
    StarDate = forms.DateField(label='Fecha Inicial', required=True,
                               widget=forms.TextInput(
                                   attrs={
                                       'placeholder': 'Fecha Inicial',
                                       'class': "form-control date-picker"
                                   }))
    EndDate = forms.DateField(label='Fecha Final',
                              widget=forms.TextInput(
                                  attrs={
                                      'placeholder': 'Fecha Final',

                                  }))


class RangeDateUserForm(forms.Form):
    StarDate = forms.DateField(label='Fecha Inicial', required=True,
                               widget=forms.TextInput(
                                   attrs={
                                       'placeholder': 'Fecha Inicial',
                                       'class': "form-control date-picker"
                                   }))
    EndDate = forms.DateField(label='Fecha Final',
                              widget=forms.TextInput(
                                  attrs={
                                      'placeholder': 'Fecha Final',

                                  }))
    user = forms.CharField(label='Usuario', required=False,
                           widget=forms.TextInput(
                               attrs={
                                   'placeholder': 'Usuario',
                               }))
