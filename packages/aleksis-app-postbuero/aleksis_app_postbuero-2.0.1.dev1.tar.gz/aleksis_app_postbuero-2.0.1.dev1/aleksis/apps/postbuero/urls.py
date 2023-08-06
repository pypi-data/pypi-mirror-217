from django.urls import path

from . import views

api_urlpatterns = [
    path(
        "api/webmilter/alias/<str:address>/",
        views.WebMilterAliasView.as_view(),
        name="webmilter_resolveAliasByAddress",
    ),
    path(
        "api/webmilter/domain/<str:domain>/alias/<str:local>/",
        views.WebMilterAliasView.as_view(),
        name="webmilter_resolveAliasByDomainAndLocalpart",
    ),
]
