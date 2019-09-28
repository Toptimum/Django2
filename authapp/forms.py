from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.forms import forms, HiddenInput, ModelForm
import random
import hashlib

from .models import ShopUser, ShopUserProfile


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'footer_subscribe_input'
            if (field_name == 'username'):
                field.widget.attrs['placeholder'] = 'Введите логин'
            if (field_name == 'password'):
                field.widget.attrs['placeholder'] = 'и пароль'
            field.label = ''  # не будем выводить лэйблы возле полей


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'password1', 'password2', 'email', 'age', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'footer_subscribe_input'
            field.help_text = ''  # здесь можно добавить свой текст помощи, который будет выводиться на форме
            if (field_name == 'username'):
                field.widget.attrs['placeholder'] = 'Придумайте логин'
            if (field_name == 'first_name'):
                field.widget.attrs['placeholder'] = 'Введите ваше имя'
            if (field_name == 'password1'):
                field.widget.attrs['placeholder'] = 'Придумайте пароль'
            if (field_name == 'password2'):
                field.widget.attrs['placeholder'] = 'повторите пароль'
            if (field_name == 'email'):
                field.widget.attrs['placeholder'] = 'Введите e-mail'
            if (field_name == 'age'):
                field.widget.attrs['placeholder'] = 'Ваш возраст'
            if (field_name != 'avatar'):
                field.label = ''  # не будем выводить лэйблы возле полей

    def clean_age(self):  # все валидаторы должны начинаться с clean
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды!")
        return data  # все валидаторы должны возвращать данные

    def save(self):
        user = super(ShopUserRegisterForm, self).save()  # создает объект пользователя и возвращает нам его
        user.is_active = False
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]  # Соль (также модификатор) —
        # строка данных, которая передаётся хеш-функции вместе с паролем.
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()  # сохранить
        return user  # и вернуть объект пользователя


class ShopUserUpdateForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'email', 'age', 'avatar',
                  'password')  # без поля password невозможно сохранить изменения

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'footer_subscribe_input'
            # Имя и Имя пользователя - это разные вещи, исправляем
            if (field_name == 'username'):
                field.label = 'Логин'
            # если поле не заполнено, то предлагаем его заполнить
            field.widget.attrs['placeholder'] = ('Введите ' + str(field.label)).capitalize()
            field.label = ''  # не будем выводить лэйблы возле полей
            field.help_text = ''  # очищаем текст помощи
            if field_name == 'password':
                field.widget = HiddenInput()  # скрываем поле пароля для конфиденциальности

    def clean_age(self):  # валидатор/проверка возраста
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды!")
        return data


class ShopUserProfileEditForm(ModelForm):
    class Meta:
        model = ShopUserProfile
        fields = ('tagline', 'aboutMe', 'gender')

    def __init__(self, *args, **kwargs):
        super(ShopUserProfileEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'footer_subscribe_input'
            # если поле не заполнено, то предлагаем его заполнить
            field.widget.attrs['placeholder'] = ('Введите ' + str(field.label)).capitalize()
            field.label = ''  # не будем выводить лэйблы возле полей
