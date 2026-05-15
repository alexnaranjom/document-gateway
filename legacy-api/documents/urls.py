from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, AuthorViewSet, DocumentViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"authors", AuthorViewSet)
router.register(r"documents", DocumentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

