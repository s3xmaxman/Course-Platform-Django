from django.shortcuts import render, redirect
from django.contrib import messages


from . import services


# Create your views here.
def verify_email_token_view(request, token, *args, **kwargs):
    """
    トークンを検証し、ユーザーを認証します。

    引数:
        request (django.http.request.HttpRequest): リクエストオブジェクト。
        token (str): 検証するトークン。

    戻り値:
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
