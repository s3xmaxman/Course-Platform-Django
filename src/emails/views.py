from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django_htmx.http import HttpResponseClientRedirect

from . import services
from .forms import EmailForm

EMAIL_ADDRESS = settings.EMAIL_ADDRESS


def logout_btn_hx_view(request):
    """
    HTMXリクエストに応じて、ログアウトボタンを提供します。

    1. HTMXリクエストでない場合は、 "/" へリダイレクトします。
    2. POSTリクエストの場合は、セッションからメールIDを削除します。
    3. メールIDが存在しない場合は、 "/" へリダイレクトします。
    4. それ以外の場合は、ログアウトボタンを出力します。

    :param request: リクエストオブジェクト
    :type request: django.http.request.HttpRequest
    :return:
    :rtype:
    """
    if not request.htmx:
        return redirect("/")
    if request.method == "POST":
        try:
            del request.session["email_id"]
        except:
            pass
        email_id_in_session = request.session.get("email_id")
        if not email_id_in_session:
            return HttpResponseClientRedirect("/")
    return render(request, "emails/hx/logout-btn.html", {})


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
    指定された検証トークンを持つEmailVerificationEventインスタンスを検証し、検証結果に基づいてログイン処理を実施します。

    1. 検証トークンを持つEmailVerificationEventインスタンスを検証します。
    2. 検証が失敗した場合は、エラーメッセージを出力し、 "/" へリダイレクトします。
    3. 検証が成功した場合は、ログイン状態を設定し、次のURL(ない場合は "/" )へリダイレクトします。

    :param request: リクエストオブジェクト
    :param token: 検証トークン
    :param args: 位置引数
    :param kwargs: キーワード引数
    :return: 302リダイレクト
    :rtype: django.http.response.HttpResponse
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
