from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from drones.models import DroneCategory, Drone, Pilot, Competition
from drones.serializer import DroneCategorySerializer, DroneSerializer, PilotSerializer, CompetitionSerializer


# Create your views here.
class DroneCategoryList(generics.ListCreateAPIView):
  queryset = DroneCategory.objects.all()
  serializer_class = DroneCategorySerializer
  name = 'dronecategory-list'


class DroneCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = DroneCategory.objects.all()
  serializer_class = DroneCategorySerializer
  name = 'dronecategory-detail'


class DroneList(generics.ListCreateAPIView):
  queryset = Drone.objects.all()
  serializer_class = DroneSerializer
  name = 'drone-list'


class DroneDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Drone.objects.all()
  serializer_class = DroneSerializer
  name = 'drone-detail'


class PilotList(generics.ListCreateAPIView):
  queryset = Pilot.objects.all()
  serializer_class = PilotSerializer
  name = 'pilot-list'


class PilotDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Pilot.objects.all()
  serializer_class = PilotSerializer
  name = 'pilot-detail'


class CompetitionList(generics.ListCreateAPIView):
  queryset = Competition.objects.all()
  serializer_class = CompetitionSerializer
  name = 'competition-list'


class CompetitionDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Competition.objects.all()
  serializer_class = CompetitionSerializer
  name = 'competition-detail'


def get(request, *args, **kwargs):
  return Response({
    'drone-categories': reverse(DroneCategoryList.name, request=request),
    'drones': reverse(DroneList.name, request=request),
    'pilots': reverse(PilotList.name, request=request),
    'competitions': reverse(CompetitionList.name, request=request)
  })


class ApiRoot(generics.GenericAPIView):
  name = 'api-root'
