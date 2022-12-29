from django.db.models import Q
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST
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
        current_eta = Expectation.objects.filter(done_at__isnull=True).first()
        closed_eta = Expectation.objects.filter(user=request.user).filter(done_at__lt=timezone.now())

        data = {
            "current": ExpectationSerializer(current_eta).data if current_eta else None,
            "closed": ExpectationSerializer(closed_eta, many=True).data,
        }
        return Response(data)

    def post(self, request):
        command = request.POST.get("command") or ""
        existed_eta = Expectation.objects.filter(user=request.user).first()
        try:
            if existed_eta:
                extends_existed_eta(command, existed_eta)
            else:
                create_new_eta(command, request.user)
        except ValueError as e:
            return Response({"detail": e.args[0]}, status=HTTP_400_BAD_REQUEST)

        return Response({"detail": "ok"})
