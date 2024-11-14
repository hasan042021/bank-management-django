from django.shortcuts import render, redirect
from django.views.generic import FormView, View
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegistrationForm, UserUpdateForm
from django.urls import reverse_lazy
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string


def send_profile_update_email(
    user,
    subject,
    template,
):
    message = render_to_string(
        template,
        {
            "user": user,
        },
    )
    send_email = EmailMultiAlternatives(subject, "", to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


# Create your views here.
class UserRegistrationView(FormView):
    template_name = "accounts/user_registration.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = "accounts/user_login.html"

    def get_success_url(self):
        return reverse_lazy("profile")


class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy("home")


class UserBankAccountUpdateView(View):
    template_name = "accounts/profile.html"

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("profile")
        return render(request, self.template_name, {"form": form})


class UserPassWordChange(LoginRequiredMixin, View):
    template_name = "accounts/password_change.html"

    def get(self, request):
        form = SetPasswordForm(user=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        print(request.user, "line 60")
        form = SetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            update_session_auth_hash(request, form.user)
            send_profile_update_email(
                request.user,
                "Password Change Message",
                "emails/pass_change_mail.html",
            )
            return redirect("profile")
        return render(request, self.template_name, {"form": form})
