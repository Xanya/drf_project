from rest_framework.routers import DefaultRouter

from products.viewsets import ProductViewSet, ListDetailViewSet

router = DefaultRouter()
router.register('products', ListDetailViewSet, basename='products')
print(router.urls)
urlpatterns = router.urls
