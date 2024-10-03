"""
cfehome プロジェクトの URL 設定

`urlpatterns` リストは URL をビューにルーティングします。詳細については、以下を参照してください。
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
例：
関数ビュー
    1. インポートを追加:  from my_app import views
    2. urlpatterns に URL を追加:  path('', views.home, name='home')
クラスベースビュー
    1. インポートを追加:  from other_app.views import Home
    2. urlpatterns に URL を追加:  path('', Home.as_view(), name='home')
別の URLconf を含める
    1. include() 関数をインポート: from django.urls import include, path
    2. urlpatterns に URL を追加:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


from django.contrib import admin
from django.urls import path

from emails.views import verify_email_token_view, email_token_login_view
from . import views

urlpatterns = [
    path("", views.home_view),
    path("login/", views.login_logout_template_view),
    path("logout/", views.login_logout_template_view),
    path("hx/login/", email_token_login_view),
    path("admin/", admin.site.urls),
    path("courses/", include("courses.urls")),
    path("verify/<uuid:token>/", verify_email_token_view),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
