from .serializers import TraineeSerializer, TraineeRecordsSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Trainees, TraineeRecords
from rest_framework import generics


class trainee_list(generics.ListCreateAPIView):
    queryset = Trainees.objects.all()
    serializer_class = TraineeSerializer


class trainee_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trainees.objects.all()
    serializer_class = TraineeSerializer


class trainee_record_list(generics.ListCreateAPIView):
    queryset = TraineeRecords.objects.all()
    serializer_class = TraineeRecordsSerializer

    def perform_create(self, serializer):
        try:
            discord_id = self.request.data['discord_id']
            trainee = Trainees.objects.get(discord_id=discord_id)
        except (KeyError, Trainees.DoesNotExist):
            return Response({"error": "Invalid or missing 'discord_id'."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(trainee=trainee)


class trainee_record_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TraineeRecords.objects.all()
    serializer_class = TraineeRecordsSerializer
