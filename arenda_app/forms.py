from django import forms
from .models import SpaceType, Space, City, RentType

space_types = SpaceType.objects.all()
SPACE_TYPES = []
for type in space_types:
    SPACE_TYPES.append((type.name, type.name))



class SelectSpaces(forms.Form):
    type = forms.ModelChoiceField(label='Тип помещения', queryset=SpaceType.objects.all(), initial=0)
    rent_type = forms.ModelChoiceField(label='Срок аренды', queryset=RentType.objects.all(), initial=0)
    city = forms.CharField(label='Город', widget=forms.TextInput(attrs={'list': 'cities', 'placeholder': 'Москва'}))

    price_from = forms.IntegerField(label='Цена от', min_value=0,
                                    widget=forms.NumberInput(attrs={'placeholder': 'руб'}),
                                    required=False)
    price_to = forms.IntegerField(label='Цена до',
                                  widget=forms.NumberInput(attrs={'placeholder': 'руб'}),
                                    required=False)
    area_from = forms.IntegerField(label='Площадь от',
                                  widget=forms.NumberInput(attrs={'placeholder': 'м²'}),
                                    required=False)
    area_to = forms.IntegerField(label='Площадь до',
                                  widget=forms.NumberInput(attrs={'placeholder': 'м²'}),
                                    required=False)