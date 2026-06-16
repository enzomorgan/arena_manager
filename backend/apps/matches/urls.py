from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import MatchViewSet, MatchEventViewSet
from .ranking_views import (
    TopScorersView,
    TopAssistsView,
    YellowCardsRankingView,
    RedCardsRankingView,
)

router = DefaultRouter()
router.register(r"matches", MatchViewSet, basename="matches")
router.register(r"match-events", MatchEventViewSet, basename="match-events")

urlpatterns = router.urls + [
    path("rankings/top-scorers/", TopScorersView.as_view(), name="top-scorers"),
    path("rankings/assists/", TopAssistsView.as_view(), name="assists-ranking"),
    path("rankings/yellow-cards/", YellowCardsRankingView.as_view(), name="yellow-cards-ranking"),
    path("rankings/red-cards/", RedCardsRankingView.as_view(), name="red-cards-ranking"),
]