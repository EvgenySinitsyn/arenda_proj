from django import forms
from .models import SpaceType, RentType, User, Space, SpaceImage, Building, City
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



space_types = SpaceType.objects.all()
SPACE_TYPES = []
for type in space_types:
    SPACE_TYPES.append((type.name, type.name))


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль:', widget=forms.PasswordInput(attrs={'class': 'form-control'}))



class SelectSpaces(forms.Form):
    type = forms.ModelChoiceField(label='Тип помещения', queryset=SpaceType.objects.all(), blank=True, required=False)
    rent_type = forms.ModelChoiceField(label='Срок аренды', queryset=RentType.objects.all(), blank=True, required=False)
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


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль:', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля:', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Телефон:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail:', widget=forms.EmailInput(attrs={'class': 'form-control'}), required=False)
    first_name = forms.CharField(label='Имя:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия:', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'phone')


# class CityForm(forms.Form):
#     city = forms.CharField(label='Город', widget=forms.TextInput(attrs={'list': 'cities', 'placeholder': 'Москва'}))

class BuildingForm(forms.ModelForm):
    city = forms.CharField(label='Город', widget=forms.TextInput(attrs={'list': 'cities', 'placeholder': 'Москва', 'class': 'form-control'}))
    street = forms.CharField(label='Улица', widget=forms.TextInput(attrs={'list': 'streets', 'class': 'form-control'}))
    number = forms.CharField(label='Дом', widget=forms.TextInput(attrs={'list': 'numbers', 'class': 'form-control'}))

    class Meta:
        model = Building
        fields = ('city', 'street', 'number')


class SpaceForm(forms.ModelForm):
    type = forms.ModelChoiceField(label='Тип помещения', queryset=SpaceType.objects.all())
    rent_type = forms.ModelChoiceField(label='Срок аренды', queryset=RentType.objects.all())

    class Meta:
        model = Space
        exclude = ('building', 'owner', 'views')



