from django.db.models import Q
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response

from apps.todo.api.eta_regex import create_new_eta, extends_existed_eta
from apps.todo.api.serializers import ExpectationSerializer
from apps.todo.models import Expectation


class OpenedEtaView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        query = Expectation.objects.filter(Q(done_at__isnull=True) | Q(done_at__gt=timezone.now()))
        return Response(ExpectationSerializer(query, many=True).data)


class UserEtaView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        current_eta = Expectation.objects.filter(done_at__isnull=True)
        closed_eta = Expectation.objects.filter(user=request.user).filter(done_at__lt=timezone.now())

        data = {
            "current": ExpectationSerializer(current_eta).data,
            "closed": ExpectationSerializer(closed_eta, many=True).data,
        }
        return Response(data)

    def post(self, request):
        command = request.POST.get("command")
        existed_eta = Expectation.objects.filter(user=request.user)
        try:
            if existed_eta:
                extends_existed_eta(command, existed_eta)
            else:
                create_new_eta(command)
        except ValueError:
            return Response({"detail": "Invalid command"})

        return Response({"detail": "ok"})
