from django.conf import settings
from django.template.loader import get_template


def get_cloudinary_image_object(
    instance, field_name="image", as_html=False, format=None, width=1200
):
    """
    インスタンスとフィールド名を受け取り、Cloudinaryの画像オブジェクトを返します。

    オプションの引数:

    - as_html: Trueの場合、画像オブジェクトをHTML（<img>タグ）として返します。
    - format: 画像のフォーマット（例： "jpg"、 "png"など）。
    - width: 画像の幅（ピクセル単位）。

    指定されたフィールドがインスタンスに存在しない場合、またはフィールドにCloudinaryの画像オブジェクトが関連付けられていない場合、空の文字列を返します。

    """

    if not hasattr(instance, field_name):
        return ""
    image_object = getattr(instance, field_name)
    if not image_object:
        return ""
    image_options = {"width": width}
    if format is not None:
        image_options["format"] = format
    if as_html:
        return image_object.image(**image_options)
    url = image_object.build_url(**image_options)
    return url


def get_cloudinary_video_object(
    instance,
    field_name="video",
    as_html=False,
    width=None,
    height=None,
    sign_url=True,  # for private videos
    fetch_format="auto",
    quality="auto",
    controls=True,
    autoplay=True,
):
    """
    インスタンスとフィールド名を受け取り、Cloudinaryの動画オブジェクトを返します。

    オプションの引数:

    - as_html: Trueの場合、動画オブジェクトをHTML（<video>タグ）として返します。
    - width: 動画の幅（ピクセル単位）。
    - height: 動画の高さ（ピクセル単位）。
    - sign_url: Trueの場合、プライベート動画に対して署名付きのURLを生成します。
    - fetch_format: 動画のフォーマット（例： "webm"、 "mp4"など）。
    - quality: 動画の品質（例： "auto"、 "sd"、 "hd"など）。
    - controls: Trueの場合、動画にコントロールバーを表示します。
    - autoplay: Trueの場合、動画を自動再生します。

    指定されたフィールドがインスタンスに存在しない場合、またはフィールドにCloudinaryの動画オブジェクトが関連付けられていない場合、空の文字列を返します。

    """
    if not hasattr(instance, field_name):
        return ""
    video_object = getattr(instance, field_name)
    if not video_object:
        return ""
    video_options = {
        "sign_url": sign_url,
        "fetch_format": fetch_format,
        "quality": quality,
        "controls": controls,
        "autoplay": autoplay,
    }
    if width is not None:
        video_options["width"] = width
    if height is not None:
        video_options["height"] = height
    if height and width:
        video_options["crop"] = "limit"
    url = video_object.build_url(**video_options)
    if as_html:
        template_name = "videos/snippets/embed.html"
        tmpl = get_template(template_name)
        cloud_name = settings.CLOUDINARY_CLOUD_NAME
        _html = tmpl.render(
            {"video_url": url, "cloud_name": cloud_name, "base_color": "#007cae"}
        )
        return _html
    return url
