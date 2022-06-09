from logging import getLogger

from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import account_activation_token, account_password_reset_token

logger = getLogger(__name__)


def create_account_activation_url(uid, token, request):
    endpoint = reverse("accounts:activate")
    protocol = "https" if request.is_secure() else "http"
    host = request.get_host()

    return f"{protocol}://{host}{endpoint}?uid={uid}&token={token}"


def send_tokenified_email(
    user,
    request,
    ctx,
    subject,
    sender=None,
    message="",
):
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    if ctx == "activation":
        token = account_activation_token
        message = "This is your email activation link: "
        subject = "Request for Account Verification"
    elif ctx == "passwordReset":
        token = account_password_reset_token
        message = "This is your password reset link: "
        subject = "Request for Password Reset"

    token = token.make_token(user)
    message += create_account_activation_url(uid, token, request)
    send_mail(
        f"{subject}",
        f"{message}",
        f"from@example.com",
        ["to@example.com"],
        fail_silently=False,
    )
