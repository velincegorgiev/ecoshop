from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from order.views import user_orders

from .forms import PwdResetForm, RegistrationForm, UserEditForm
from .models import UserBase
from .tokens import account_activation_token


@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(data=request.POST, files=request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect("/account/dashboard/")

    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, 'account/user/edit_details.html', {'user_form': user_form})


@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request, 'account/user/dashboard.html', {'orders': orders})


@login_required
def delete_user(request):
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    user.delete()
    return redirect('account:delete_confirm')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PwdResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            user = UserBase.objects.get(email=data)

            # Current site
            current_site = get_current_site(request)
            subject = "Password Reset Requested"
            message = render_to_string("account/user/password_reset_email.html", {
                "email": user.email,
                'domain': current_site.domain,
                'site_name': 'Website',
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                'token': default_token_generator.make_token(user),
                'protocol': 'http',
            })
            email_from = settings.EMAIL_HOST_USER
            send_mail(subject, message, email_from, [user.email], fail_silently=False)

            return redirect("/account/password_reset/password_reset_email_confirm/")
    else:
        password_reset_form = PwdResetForm()
    return render(request=request, template_name="account/user/password_reset_form.html", context={"form": password_reset_form})


def account_register(request):
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            # Current site
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/account_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('registered succesfully and activation sent')
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)

    except():
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')


def page_not_found_view(request, exception):
    return render(request, 'error/404.html', status=404)
