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
        fields = ['discord_id', 'discord_pfp', 'last_activity', 'discord_name', 'total_days',
                  'total_problems', 'highest_streak', 'current_streak', 'trainee_records']

    def create(self, validated_data):
        validated_data['total_days'] = 0
        validated_data['total_problems'] = 0
        validated_data['highest_streak'] = 0
        validated_data['current_streak'] = 0
        return super().create(validated_data)
