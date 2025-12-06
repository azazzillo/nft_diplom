from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework.routers import DefaultRouter

from .views import LoginRegisterViewSet, to_login


# router= DefaultRouter()

# router.register(r'login', LoginRegisterViewSet, basename='login')


urlpatterns = [
    path('', LoginRegisterViewSet.as_view({'get': 'list'}), name='login'),
    path('to_login/', to_login, name='to_login')
    # Другие маршруты...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # path('', include(router.urls), name='login'),
    # path('auth_with_metamask/', auth_with_metamask, name='auth_with_metamask'),
    # path('in/', LoginRegisterViewSet.as_view({'post':'metamask_auth'},), name='metamask_auth')

