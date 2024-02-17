
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Trainee, TraineeRecord
from .serializers import TraineeSerializer, TraineeRecordSerializer


class TraineeListCreateView(generics.ListCreateAPIView):
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer


class TraineeDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trainee.objects.all()
    serializer_class = TraineeSerializer


class TraineeRecordListCreateView(generics.ListCreateAPIView):
    queryset = TraineeRecord.objects.all()
    serializer_class = TraineeRecordSerializer

    def perform_create(self, serializer):
        try:
            discord_id = self.request.data['discord_id']
            trainee = Trainee.objects.get(discord_id=discord_id)
        except (KeyError, Trainee.DoesNotExist):
            return Response({"error": "Invalid or missing 'discord_id'."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(trainee=trainee)


class TraineeRecordDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TraineeRecord.objects.all()
    serializer_class = TraineeRecordSerializer
