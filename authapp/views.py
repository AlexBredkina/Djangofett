from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm, ShopUserProfileEditForm
from django.contrib import auth, messages
from django.urls import reverse

from authapp.models import User
from basketapp.models import Basket


# Create your views here.

def send_verify_email(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])
    subject = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения перейдите по ссылке {settings.DOMAIN}{verify_link}'
    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            # user.activation_key = None
            user.save()
            auth.login(request, user)
        return render(request, 'authapp/verification.html')
    except Exception as ex:
        return HttpResponseRedirect(reverse('main'))


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            send_verify_email(user)
            messages.success(request, 'Вы успешно зарегистрировались')
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'authapp/register.html', context)


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(data=request.POST, instance=request.user.shopuserprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:profile'))
    else:
        form = UserProfileForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)

    # total_quantity =0
    # for basket in Basket.objects.filter(user = request.user):
    #     total_quantity+=1
    # total_sum = 0
    # for basket in Basket.objects.filter(user=request.user):
    #     total_sum+=basket.sum()
    context = {
        'title': 'Профиль',
        'form': form,
        'baskets': Basket.objects.filter(user=request.user),
        'profile_form': profile_form,
        # 'total_quantity': total_quantity,
        # 'total_sum': total_sum,
        # 'total_quantity': sum(basket.quantity for basket in Basket.objects.filter(user = request.user)),
        # 'total_sum': sum(basket.sum() for basket in Basket.objects.filter(user = request.user)),

    }
    return render(request, 'authapp/profile.html', context)
