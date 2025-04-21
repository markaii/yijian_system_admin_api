from __future__ import unicode_literals
from help import views
from django.conf.urls import url, include
from django.urls import path

from rest_framework import routers

router = routers.DefaultRouter()
router.register('article', views.HelpArticleViewSet)     # 帮助中心文章API /help/article/
router.register('category', views.HelpCategoryViewSet)   # 文章分类API /help/category/
# router.register('feedback/attachment', views.HelpFeedbackAttachmentViewSet)
router.register('feedback/comment', views.HelpFeedbackCommentViewSet)  # 反馈回复API /help/feedback/commect/
router.register('feedback', views.HelpFeedbackViewSet)   # 问题反馈API /help/feedback/
urlpatterns = [
    url(r'^', include(router.urls)),
]
