from django.shortcuts import render
from django.conf import settings
from emails import services as emails_services
from emails.forms import EmailForm

EMAIL_ADDRESS = settings.EMAIL_ADDRESS


def login_logout_template_view(request, *args, **kwargs):
    return render(request, "auth/login-logout.html", {})


def home_view(request, *args, **kwargs):
    """
    ホームビューを処理し、home.htmlテンプレートをレンダリングし、メールフォームからのPOSTリクエストを処理します。

    フォームが有効な場合、メールサービスを使用して検証イベントを開始し、フォームをリセットします。

    フォームが無効な場合、フォームのエラーを出力します。

    また、セッションにメールIDが存在する場合は、それを出力します。

    :param request: リクエストオブジェクト
    :param args: 位置引数
    :param kwargs: キーワード引数
    :return: レンダリングされたレスポンス
    """
    template_name = "home.html"
    form = EmailForm(request.POST or None)
    context = {"form": form, "message": ""}
    if form.is_valid():
        email_val = form.cleaned_data.get("email")
        obj = emails_services.start_verification_event(email_val)
        context["form"] = EmailForm()
        context["message"] = (
            f"Succcess! Check your email for verification from {EMAIL_ADDRESS}"
        )
    else:
        print(form.errors)
    print("email_id", request.session.get("email_id"))
    return render(request, template_name, context)
