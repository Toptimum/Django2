from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.forms import HiddenInput, ModelForm
from django import forms
from authapp.models import ShopUser
from mainapp.models import Categories, Products


class ShopUserAdminCreateForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'password1', 'password2', 'email', 'age', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''  # здесь можно добавить свой текст помощи, который будет выводиться на форме

    def clean_age(self):  # все валидаторы должны начинаться с clean
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды!")

        return data  # все валидаторы должны возвращать данные


class ShopUserAdminUpdateForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name', 'email', 'age', 'avatar',
                  'password', 'is_superuser', 'is_active')  # без поля password невозможно сохранить изменения

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''  # очищаем текст помощи
            if field_name == 'password':
                field.widget = HiddenInput()  # скрываем поле пароля для конфиденциальности

    def clean_age(self):  # валидатор/проверка возраста
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды!")

        return data


class CategoriesAdminUpdateForm(ModelForm):
    # Чтобы избежать проблем с валидацией мы задали аргумент required=False
    discount = forms.IntegerField(label='Скидка на товары', required=False, min_value=0, max_value=90, initial=0)

    class Meta:
        model = Categories
        # fields = '__all__'
        # exclude кортеж с исключенными из отображения полями
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductAdminUpdateForm(ModelForm):
    class Meta:
        model = Products
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
