from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ChampionshipViewSet, StandingViewSet
from .dashboard_views import ChampionshipDashboardView
from .generate_views import GenerateMatchesView

router = DefaultRouter()
router.register(r"championships", ChampionshipViewSet, basename="championships")
router.register(r"standings", StandingViewSet, basename="standins")

urlpatterns = router.urls + [
    path(
        "championships/<int:championship_id>/dashboard/",
        ChampionshipDashboardView.as_view(),
        name="championship-dashboard",
    ),
    path(
    "championships/<int:championship_id>/generate-matches/",
    GenerateMatchesView.as_view(),
    name="generate-matches",
),
]