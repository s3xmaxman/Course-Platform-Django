from cloudinary import CloudinaryImage
from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "access"]
    list_filter = ["status", "access"]
    fields = [
        "title",
        "description",
        "image",
        "status",
        "access",
        "display_image",
    ]
    readonly_fields = ["display_image"]

    def display_image(self, obj, *args, **kwargs):
        return format_html(f"<img src='{obj.image_admin}' />")


# admin.site.register(Course)
