from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ChampionshipViewSet, StandingViewSet
from .dashboard_views import ChampionshipDashboardView
from .generate_views import GenerateMatchesView
from .recalculate_views import RecalculateStandingsView
from .stats_views import TopScorersView

router = DefaultRouter()
router.register(r"championships", ChampionshipViewSet, basename="championships")
router.register(r"standings", StandingViewSet, basename="standings")

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
    path(
    "championships/<int:championship_id>/recalculate/",
    RecalculateStandingsView.as_view(),
    name="recalculate-standings",
    ),
    path(
    "championships/<int:championship_id>/top-scorers/",
    TopScorersView.as_view(),
    name="top-scorers",
    ),
]