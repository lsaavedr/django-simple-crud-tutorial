# cats/urls.py
from rest_framework.routers import SimpleRouter

from cats.views import CatViewSet

router = SimpleRouter()
router.register("cats", CatViewSet)

urlpatterns = router.get_urls()
