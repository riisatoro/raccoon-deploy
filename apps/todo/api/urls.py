from django.urls import path

from apps.todo.api.views import OpenedEtaView, UserEtaView

urlpatterns = [
    path("eta/", OpenedEtaView.as_view(), name="opened_eta"),
    path("eta/my/", UserEtaView.as_view(), name="user_eta"),
]
