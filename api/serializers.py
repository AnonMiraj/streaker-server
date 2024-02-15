from rest_framework import serializers
from .models import Trainees, TraineeRecords


class TraineeRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TraineeRecords
        fields = ['id', 'discord_id', 'post_date', 'message', 'streak', 'today_problems']



class TraineeSerializer(serializers.HyperlinkedModelSerializer):
    trainee_records = TraineeRecordsSerializer(many=True, read_only=True)

    class Meta:
        model = Trainees
        fields = ['discord_id', 'discord_pfp', 'discord_name', 'total_days',
                  'total_problems', 'highest_streak', 'current_streak', 'trainee_records']
