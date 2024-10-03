from django.shortcuts import render
from django.http import Http404, JsonResponse
from . import services
import helpers

# Create your views here.


def course_list_view(request):
    """
    公開されたコースの一覧を表示します。

    このビューは、タイトル、説明、および詳細ページへのリンクを含むすべての公開されたコースの一覧を返します。

    :param request: Django リクエストオブジェクト
    :return: Django レスポンスオブジェクト
    """

    queryset = services.get_publish_courses()
    context = {
        "object_list": queryset,
    }
    return render(request, "courses/list.html", context)


def course_detail_view(
    request,
    course_id=None,
    *args,
    **kwargs,
):
    """
    このビューは、コースの詳細ページを表示するために使用されます。

    ビューは、course_id パラメータを受け取り、それを使用してデータベースからコースオブジェクトを取得します。
    コースオブジェクトは、コースに関連するレッスンを取得するために使用されます。
    コースオブジェクトとレッスンのクエリセットは、コースの詳細テンプレートに渡されます。

    コースオブジェクトが見つからない場合、ビューは 404 例外を発生させます。

    :param request: リクエストオブジェクト
    :param course_id: 表示するコースの public_id
    :return: レンダリングされたコース詳細テンプレート
    """
    course_obj = services.get_course_detail(course_id=course_id)
    if course_obj is None:
        raise Http404
    lessons_queryset = services.get_course_lessons(course_obj=course_obj)
    context = {
        "object": course_obj,
        "lessons_queryset": lessons_queryset,
    }
    return render(request, "courses/detail.html", context)


def lesson_detail_view(
    request,
    course_id=None,
    lesson_id=None,
    *args,
    **kwargs,
):
    """
    レッスンの詳細ビューを処理します。

    Args:
        request (HttpRequest): リクエストオブジェクト。
        course_id (int, optional): コースのID。デフォルトはNone。
        lesson_id (int, optional): レッスンのID。デフォルトはNone。
        *args: 位置引数。
        **kwargs: キーワード引数。

    Returns:
        HttpResponse: レンダリングされたレスポンス。

    1. コースIDとレッスンIDを使用して、レッスンの詳細を取得します。
    2. レッスンが存在しない場合は404エラーを発生させます。
    3. レッスンがメールアドレスを必要とする場合、セッションにメールIDが存在しない場合は、メールアドレス入力ページにリダイレクトします。
    4. レッスンが「Coming Soon」でないかつビデオがある場合は、ビデオの埋め込みHTMLを取得し、テンプレートを設定します。
    5. レンダリングされたレスポンスを返します。
    """

    lesson_obj = services.get_lesson_detail(course_id=course_id, lesson_id=lesson_id)
    if lesson_obj is None:
        raise Http404
    email_id_exists = request.session.get("email_id")
    if lesson_obj.requires_email and not email_id_exists:
        request.session["next_url"] = request.path
        return render(request, "courses/email-required.html", {})
    template_name = "courses/lesson-coming-soon.html"
    context = {"object": lesson_obj}
    if not lesson_obj.is_coming_soon and lesson_obj.has_video:
        template_name = "courses/lesson.html"
        video_embed_html = helpers.get_cloudinary_video_object(
            lesson_obj,
            field_name="video",
            as_html=True,
            width=1250,
        )
        context["video_embed"] = video_embed_html
    return render(request, template_name, context)
