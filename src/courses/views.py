from django.shortcuts import render
from django.http import Http404, JsonResponse
from . import services
import helpers

# Create your views here.


def course_list_view(request):
    queryset = services.get_publish_courses()
    context = {
        "object_list": queryset,
    }
    return render(request, "courses/list.html", context)


def course_detail_view(request, course_id=None, *args, **kwargs):
    course_obj = services.get_course_detail(course_id=course_id)
    if course_obj is None:
        raise Http404
    lessons_queryset = services.get_course_lessons(course_obj=course_obj)
    context = {
        "object": course_obj,
        "lessons_queryset": lessons_queryset,
    }
    return render(request, "courses/detail.html", context)


def lesson_detail_view(request, course_id=None, lesson_id=None, *args, **kwargs):
    lesson_obj = services.get_lesson_detail(
        course_id=course_id,
        lesson_id=lesson_id,
    )
    if lesson_obj is None:
        raise Http404
    template_name = "courses/lesson-coming-soon.html"
    context = {
        "object": lesson_obj,
    }
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
