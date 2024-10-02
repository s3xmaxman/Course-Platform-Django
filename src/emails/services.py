from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from .models import Email, EmailVerificationEvent

EMAIL_HOST_USER = settings.EMAIL_HOST_USER


def verify_email(email):
    """
    メールアドレスが確認済みかどうかを示すブール値を返します。

    Args:
        email (str): 確認するメールアドレス

    Returns:
        bool: メールアドレスが確認済みかどうか
    """
    qs = Email.objects.filter(email=email, active=False)
    return qs.exists()


def get_verification_email_msg(verification_instance, as_html=False):
    """
    検証インスタンスに基づいて検証メールメッセージを生成します。

    Args:
        verification_instance (EmailVerificationEvent): 検証インスタンス
        as_html (bool, optional): HTML形式で生成するかどうか. Defaults to False.

    Returns:
        str: 検証メールメッセージ

    Raises:
        TypeError: verification_instanceがEmailVerificationEventインスタンスでない場合
    """
    if not isinstance(verification_instance, EmailVerificationEvent):
        raise TypeError(
            "verification_instanceはEmailVerificationEventインスタンスである必要があります。"
        )
    verify_link = verification_instance.get_link()
    if as_html:
        return f"<h1>以下のリンクでメールアドレスを確認してください</h1><p><a href='{verify_link}'>{verify_link}</a></p>"
    return f"以下のリンクでメールアドレスを確認してください:\n{verify_link}"


def start_verification_event(email):
    """
    メールアドレスの検証イベントを開始します。

    1. 指定されたメールアドレスのEmailインスタンスを取得または作成します。
    2. EmailインスタンスのEmailVerificationEventインスタンスを作成します。
    3. 検証IDを含む検証メールを送信します。
    4. EmailVerificationEventインスタンスと、検証メールが正常に送信されたかどうかを示すブール値を返します。

    Args:
        email (str): 検証を開始するメールアドレス

    Returns:
        tuple: EmailVerificationEventインスタンスと、検証メールが正常に送信されたかどうかを示すブール値
    """
    email_obj, created = Email.objects.get_or_create(email=email)
    obj = EmailVerificationEvent.objects.create(
        parent=email_obj,
        email=email,
    )
    sent = send_verification_email(obj.id)
    return obj, sent


def send_verification_email(verify_obj_id):
    """
    指定された検証IDを持つユーザーに検証メールを送信します。

    Args:
        verify_obj_id (int): 検証メールを送信するEmailVerificationEventインスタンスのID

    Returns:
        bool: 検証メールが正常に送信されたかどうか
    """
    verify_obj = EmailVerificationEvent.objects.get(id=verify_obj_id)
    email = verify_obj.email
    subject = "メールアドレスを確認してください"
    text_msg = get_verification_email_msg(verify_obj, as_html=False)
    text_html = get_verification_email_msg(verify_obj, as_html=True)
    from_user_email_address = EMAIL_HOST_USER
    to_user_email_address = email
    return send_mail(
        subject,
        text_msg,
        from_user_email_address,
        [to_user_email_address],
        fail_silently=False,
        html_message=text_html,
    )
