from django.core.mail import send_mail
from django.conf import settings
from django.contrib import auth
from django.db import transaction
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from authapp.models import ShopUser
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserUpdateForm, ShopUserProfileEditForm
from mainapp.views import main_menu, footer_menu, get_basket


# Create your views here.

def login(request):
    # если не делать условие, то когда не будет next - будет ошибка
    next = request.GET['next'] if 'next' in request.GET.keys() else None
    if request.method == 'POST':
        # форма заполнится данными
        form = ShopUserLoginForm(data=request.POST)  # data используется для работы с AuthenticationForm
        if form.is_valid():  # проверили валидность введенных данных и вывод сообщений об ошибках
            username = request.POST['username']  # получаем логин и пароль
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:  # активирован ли аккаунт
                next = request.POST['next'] if 'next' in request.POST.keys() else None
                auth.login(request, user)
                return HttpResponseRedirect('/' if not next else next)  # первый вариант редиректа
    else:
        form = ShopUserLoginForm()
    context = {
        'title': 'Авторизация на сайте',
        'form': form,
        'next': next,
        'main_menu': main_menu(),
        'info_pages': footer_menu(),
        'basket': get_basket(request),
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:main'))  # второй вариант боле правильный редирект через пространство имен


def register(request):
    if request.method == 'POST':
        form = ShopUserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # приводит к сохранению в базу данных
            if send_verify_mail(user):
                print('Сообщение успешно отправлено!')
                return HttpResponseRedirect(reverse('authapp:login'))
            else:
                print('Ошибка: сообщение не отправлено.')
                return HttpResponseRedirect(reverse('authapp:login'))
    else:
        form = ShopUserRegisterForm()
        content = {'title': 'Регистрация', 'form': form}
        return render(request, 'authapp/register.html', content)

    content = {
        'title': 'Регистрация пользователя',
        'form': form,
        'main_menu': main_menu(),
        'info_pages': footer_menu(),
        'basket': get_basket(request),
    }

    return render(request, 'authapp/register.html', content)


def send_verify_mail(user):
    verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} на сайте {settings.DOMAIN_NAME} перейдите по ссылке: ' \
              f'\n{settings.DOMAIN_NAME}{verify_link}'
    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email],
                     fail_silently=False)  # в случае неудачной отправки, генерируется ошибка


def verify(request, email, activation_key):
    content = {
        'title': 'Активация пользователя',
        'main_menu': main_menu(),
        'info_pages': footer_menu(),
        'basket': get_basket(request),
    }
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html', content)
        else:
            print(f'При активации пользователя {user} произошла ошибка.')
            return render(request, 'authapp/verification.html', content)
    except Exception as e:
        print(f'Ошибка при активации пользователя: {e.args}')
        return render(request, 'authapp/verification.html', content)


@login_required
def update(request):
    if request.method == 'POST':
        # в instance передаем существующий объект пользователя для редактирования
        form = ShopUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:update'))
    else:
        form = ShopUserUpdateForm(instance=request.user)
    content = {
        'title': 'Редактирование данных',
        'form': form,
        'main_menu': main_menu(),
        'info_pages': footer_menu(),
        'basket': get_basket(request),
    }
    return render(request, 'authapp/update.html', content)


# изменения сохраняются в двух моделях, для обеспечения целостности данных применяем к контроллеру декоратор
@transaction.atomic
def update(request):
    if request.method == 'POST':
        form = ShopUserUpdateForm(request.POST, request.FILES, instance=request.user)
        # она заполняется данными из связанной модели
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:update'))
    else:
        form = ShopUserUpdateForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)
    content = {
        'title': 'Редактирование данных',
        'form': form,
        'profile_form': profile_form,
        'main_menu': main_menu(),
        'info_pages': footer_menu(),
        'basket': get_basket(request),
    }
    return render(request, 'authapp/update.html', content)
