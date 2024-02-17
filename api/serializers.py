from rest_framework import serializers
from .models import Trainee, TraineeRecord


class TraineeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TraineeRecord 
        fields = ['id', 'discord_id', 'post_date', 'message', 'streak', 'today_problems']


class TraineeSerializer(serializers.HyperlinkedModelSerializer):
    trainee_records = TraineeRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Trainee
        fields = ['discord_id', 'discord_pfp', 'discord_name', 'last_activity', 'total_days',
                  'total_problems', 'highest_streak', 'current_streak', 'trainee_records']
        read_only_fields = ['last_activity', 'total_days', 'total_problems', 'highest_streak', 'current_streak']
