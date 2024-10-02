from django.db import models
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
import helpers
import uuid


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


def generate_public_id(instance, *args, **kwargs):
    """
    Cloudinary の public_id を生成します。

    コースのタイトルから slug を生成し、UUID の一部を組み合わせます。
    タイトルが存在しない場合は、UUID のみを使用します。

    Args:
        instance: Course インスタンス
        *args: その他の引数
        **kwargs: その他のキーワード引数

    Returns:
        str: 生成された public_id
    """

    title = instance.title
    unique_id = str(uuid.uuid4()).replace("-", "")
    if not title:
        return unique_id
    slug = slugify(title)
    unique_id_short = unique_id[:5]
    return f"{slug}-{unique_id_short}"


def get_public_id_prefix(instance, *args, **kwargs):
    """
    Cloudinary の public_id のプレフィックスを生成します。

    もしインスタンスが path 属性を持つ場合、その path をプレフィックスとして使用します。
    path の先頭と末尾のスラッシュは削除されます。

    もしインスタンスが path 属性を持たない場合、public_id とモデル名からプレフィックスを生成します。
    public_id が存在しない場合は、モデル名のみを使用します。

    Args:
        instance: モデルインスタンス
        *args: その他の引数
        **kwargs: その他のキーワード引数

    Returns:
        str: 生成された public_id プレフィックス
    """
    if hasattr(instance, "path"):
        path = instance.path
        if path.startswith("/"):
            path = path[1:]
        if path.endswith("/"):
            path = path[:-1]
        return path
    public_id = instance.public_id
    model_class = instance.__class__
    model_name = model_class.__name__
    model_name_slug = slugify(model_name)
    if not public_id:
        return f"{model_name_slug}"
    return f"{model_name_slug}/{public_id}"


def get_display_name(instance, *args, **kwargs):
    if hasattr(instance, "get_display_name"):
        return instance.get_display_name()
    elif hasattr(instance, "title"):
        return instance.title
    model_class = instance.__class__
    model_name = model_class.__name__
    return f"{model_name} Upload"


class Course(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    public_id = models.CharField(max_length=130, blank=True, null=True, db_index=True)
    image = CloudinaryField(
        "image",
        null=True,
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,
        tags=["courses", "thumbnail"],
    )
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
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.public_id == "" or self.public_id is None:
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.path

    @property
    def path(self):
        return f"/courses/{self.public_id}"

    def get_display_name(self):
        return f"{self.title} - Course"

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    public_id = models.CharField(max_length=130, blank=True, null=True, db_index=True)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    thumbnail = CloudinaryField(
        "image",
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,
        tags=["thumbnail", "lesson"],
        blank=True,
        null=True,
    )
    video = CloudinaryField(
        "video",
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,
        tags=["videos", "lesson"],
        type="private",
        blank=True,
        null=True,
        resource_type="video",
    )
    order = models.IntegerField(default=0)
    preview = models.BooleanField(default=False)
    can_preview = models.BooleanField(
        default=False, help_text="If user doesn't have access"
    )
    status = models.CharField(
        max_length=10,
        choices=PublishStatus.choices,
        default=PublishStatus.PUBLISHED,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-updated"]

    def save(self, *args, **kwargs):
        if self.public_id == "" or self.public_id is None:
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return self.path

    @property
    def path(self):
        course_path = self.course.path
        if course_path.endswith("/"):
            course_path = course_path[:-1]
        return f"{course_path}/lessons/{self.public_id}"

    def get_display_name(self):
        return f"{self.title} - {self.course.get_display_name()}"

    @property
    def is_coming_soon(self):
        return self.status == PublishStatus.COMING_SOON
