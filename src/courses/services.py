from .models import Course, PublishStatus, Lesson
from django.db.models import Q


def get_publish_courses():
    """
    公開されているコースオブジェクトのクエリセットを返します。

    返されるクエリセットは、公開されているコースのみが含まれるようにフィルタリングされます。
    """

    return Course.objects.filter(is_published=True)


def get_course_detail(course_id=None):
    """
    指定されたcourse_idを持つコースオブジェクトが存在し、公開されている場合、それを返します。

    course_idがNoneの場合、Noneを返します。

    返されるオブジェクトは、公開されているコースのみが表示されるようにフィルタリングされます。

    :param course_id: 取得するコースのpublic_id。
    :return: 見つかった場合はコースオブジェクト、そうでない場合はNone。
    """

    if course_id is None:
        return None
    obj = None
    try:
        obj = Course.objects.get(
            status=PublishStatus.PUBLISHED,
            public_id=course_id,
        )
    except:
        pass
    return obj


def get_course_lessons(course_obj=None):
    """
    指定されたコースオブジェクトのレッスンのクエリセットを返します。

    コースオブジェクトがCourse型でない場合、空のクエリセットが返されます。

    クエリセットは、公開されているか近日公開予定のレッスンのみが表示され、
    公開されているコースの下にあるようにフィルタリングされます。

    :param course_obj: レッスンを取得するコースオブジェクト。
    :return: レッスンオブジェクトのクエリセット。
    """
    lessons = Lesson.objects.none()
    if not isinstance(course_obj, Course):
        return lessons
    lessons = course_obj.lesson_set.filter(
        course__status=PublishStatus.PUBLISHED,
        status__in=[PublishStatus.PUBLISHED, PublishStatus.COMING_SOON],
    )
    return lessons


def get_lesson_detail(course_id=None, lesson_id=None):
    """
    指定されたcourse_idとlesson_idでレッスンオブジェクトを取得します。

    指定されたcourse_idとlesson_idでデータベースからレッスンオブジェクトを取得します。
    レッスンオブジェクトは、公開されているコースに属している必要があり、
    レッスンオブジェクトのステータスは「公開済み」または「近日公開予定」のいずれかである必要があります。

    :param course_id: レッスンを取得するコースのpublic_id。
    :param lesson_id: 取得するレッスンのpublic_id。
    :return: 見つかった場合はレッスンオブジェクト、そうでない場合はNone。
    """
    if lesson_id is None or course_id is None:
        return None
    obj = None
    try:
        obj = Lesson.objects.get(
            course__public_id=course_id,
            course__status=PublishStatus.PUBLISHED,
            status__in=[PublishStatus.PUBLISHED, PublishStatus.COMING_SOON],
            public_id=lesson_id,
        )
    except Exception as e:
        print(e)
        pass
    return obj
