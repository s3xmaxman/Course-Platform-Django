from django.db import models
from cloudinary.models import CloudinaryField
import helpers


helpers.cloudinary_init()


# Create your models here.
class AccessRequirement(models.TextChoices):
    ANYONE = "any", "anyone"
    EMAIL_REQUIRED = "email", "Email required"


class PublishStatus(models.TextChoices):
    PUBLISHED = "publish", "Published"
    COMING_SOON = "soon", "Coming Soon"
    DRAFT = "draft", "Draft"


def handle_upload(instance, filename):
    return f"{filename}"


# from courses.models import Course
# Course.objects.all() -> list out all courses
# Course.objects.first() -> first row of all courses


class Course(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    # image = models.ImageField(
    #     upload_to=handle_upload,
    #     null=True,
    #     blank=True,
    # )
    image = CloudinaryField("image", null=True)
    access = models.CharField(
        max_length=5,
        choices=AccessRequirement.choices,
        default=AccessRequirement.ANYONE,
    )
    status = models.CharField(
        max_length=10,
        choices=PublishStatus.choices,
        default=PublishStatus.DRAFT,
    )

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED

    @property
    def image_admin(self):
        if not self.image:
            return ""

        image_options = {"width": 200}

        url = self.image.url.build_url(**image_options)
        return url

    def image_thumbnail(self, as_html=False, width=500):
        if not self.image:
            return ""

        image_options = {"width": width}

        if as_html:
            url = self.image.url.image(**image_options)

        url = self.image.url.build_url(**image_options)
        return url
