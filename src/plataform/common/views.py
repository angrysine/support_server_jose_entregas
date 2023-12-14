from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Log
from .serializers import LogSerializer

class HomeView(TemplateView):
    template_name = 'home.jinja'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class LogsView(TemplateView):
    template_name = 'logs.jinja'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        logs_from_database = Log.objects.all()

        context['logs'] = [
            {
                "user": {
                    "name": entry.requester_name,
                    "number": entry.requester_number
                },
                "item": {
                    "description": entry.item,
                    "category": entry.category,
                },
                "request": {
                    "quantity": entry.quantity,
                    "unit": "Unidades",
                },
                "created_at": {
                    "date": entry.date.date(),
                    "time": entry.date.time(),
                },
                "status": entry.Status(entry.status).name,
            }
            for entry in logs_from_database
        ]
        return context

@api_view(['POST'])
def create_log(request):
    if request.method == 'POST':
        data = request.data
        serializer = LogSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def update_status(request):
    if request.method == 'POST':
        data = request.data
        id = data['id']
        new_status = data['status']
        log = Log.objects.get(id=id)
        log.status = new_status
        log.save()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
