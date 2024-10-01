import helpers
from cloudinary import CloudinaryImage
from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import Course, Lesson


class LessonInline(admin.TabularInline):
    model = Lesson
    readonly_fields = [
        "public_id",
        "updated",
        "display_image",
    ]
    extra = 0

    def display_image(self, obj, *args, **kwargs):
        url = helpers.get_cloudinary_image_object(
            obj,
            field_name="thumbnail",
            width=200,
        )
        return format_html(f"<img src={url} />")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ["title", "status", "access"]
    list_filter = ["status", "access"]
    fields = [
        "public_id",
        "title",
        "description",
        "image",
        "status",
        "access",
        "display_image",
    ]
    readonly_fields = ["public_id", "display_image"]

    def display_image(self, obj, *args, **kwargs):
        url = helpers.get_cloudinary_image_object(
            obj,
            field_name="image",
            width=200,
        )
        return format_html(f"<img src={url} />")


# admin.site.register(Course)
