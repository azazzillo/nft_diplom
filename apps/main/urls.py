from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter


from .views import (
    NftMainPageViewSet, to_logout, NftViewSet,
    ProfileViewSet, create_nft, new_auction,
    auc
    
)

router = DefaultRouter()

router.register(r'main', NftMainPageViewSet)


urlpatterns = [
    path('', include(router.urls), name='main'),
    path('logoutt/', to_logout, name='logoutt'),
    path('profile/', ProfileViewSet.as_view({'get':'list'}), name='profile'),
    path('creatte/', create_nft, name='creatte'),
    path('start_auction/', new_auction, name='start_auction'),
    path('nft_all/', NftViewSet.as_view({'get':'list'}), name='nft_all'),
    path('<int:auc_id>/', auc, name='auc_id')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


