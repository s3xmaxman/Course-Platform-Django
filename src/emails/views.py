from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .forms import EmailForm


from . import services

EMAIL_ADDRESS = settings.EMAIL_ADDRESS


# Create your views here.
def email_token_login_view(request):
    """
    HTMXリクエストに応じて、メールアドレスの検証フォームを提供します。

    1. HTMXリクエストでない場合は、 "/" へリダイレクトします。
    2. メールアドレスの検証フォームを出力します。
    3. フォームが有効な場合、メールアドレスの検証を開始します。
    4. フォームが無効な場合、エラーメッセージを出力します。

    :param request: リクエストオブジェクト
    :type request: django.http.request.HttpRequest
    :return:
    :rtype:
    """
    if not request.htmx:
        return redirect("/")
    email_id_in_session = request.session.get("email_id")
    template_name = "emails/hx/form.html"
    form = EmailForm(request.POST or None)
    context = {
        "form": form,
        "message": "",
        "show_form": not email_id_in_session,
    }
    if form.is_valid():
        email_val = form.cleaned_data.get("email")
        obj = services.start_verification_event(email_val)
        context["form"] = EmailForm()
        context["message"] = (
            f"Success! Check your email for verification from {EMAIL_ADDRESS}"
        )
        return render(request, template_name, context)
    else:
        print(form.errors)
    return render(request, template_name, context)


def verify_email_token_view(request, token, *args, **kwargs):
    """
    トークンを検証し、ユーザーを認証します。

    args:
        request (django.http.request.HttpRequest): リクエストオブジェクト。
        token (str): 検証するトークン。

    returns:
        django.http.response.HttpResponse: トークンが有効な場合は次のURLにリダイレクトし、
            そうでない場合は/login/にリダイレクトします。
    """
    did_verify, msg, email_obj = services.verify_token(token)
    if not did_verify:
        try:
            del request.session["email_id"]
        except:
            pass
        messages.error(request, msg)
        return redirect("/login/")
    messages.success(request, msg)
    request.session["email_id"] = f"{email_obj.id}"
    next_url = request.session.get("next_url") or "/"
    if not next_url.startswith("/"):
        next_url = "/"
    return redirect(next_url)
