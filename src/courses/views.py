from django.shortcuts import render
from django.http import Http404, JsonResponse
from . import services

# Create your views here.


def courses_list_view(request):
    queryset = services.get_publish_courses()
    context = {
        "object_list": queryset,
    }
    return render(request, "courses/list.html")


def courses_detail_view(request, course_id=None, *args, **kwargs):
    course_obj = services.get_course_detail(course_id=course_id)
    if course_obj is None:
        raise Http404
    lessons_queryset = services.get_course_lessons(course_obj=course_obj)
    context = {
        "object": course_obj,
        "lessons_queryset": lessons_queryset,
    }
    return render(request, "courses/detail.html", context)


def Lesson_detail_view(request, course_id=None, lesson_id=None, *args, **kwargs):
    lesson_obj = services.get_lesson_detail(
        course_id=course_id,
        lesson_id=lesson_id,
    )
    if lesson_obj is None:
        raise Http404
    template_name = "courses/lesson-coming-soon.html"
    if not lesson_obj.is_coming_soon:
        template_name = "courses/lesson.html"
    context = {"object": lesson_obj}
    return render(request, template_name, context)
