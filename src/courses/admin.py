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
        print(obj.image.url)
        cloudinary_id = str(obj.image)
        cloudinary_html = CloudinaryImage(cloudinary_id).image(width=500, height=500)
        return format_html(cloudinary_html)


# admin.site.register(Course)
