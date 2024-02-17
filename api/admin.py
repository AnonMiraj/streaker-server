from django.contrib import admin
from .models import Trainee, TraineeRecord

@admin.register(Trainee)
class TraineeAdmin(admin.ModelAdmin):
    list_display = ('discord_id', 'discord_name', 'last_activity', 'total_days',
                    'total_problems', 'highest_streak', 'current_streak')
    list_filter = ('last_activity',)
    search_fields = ('discord_id', 'discord_name')
    readonly_fields = ('last_activity', 'total_days', 'total_problems', 'highest_streak', 'current_streak')

@admin.register(TraineeRecord)
class TraineeRecordAdmin(admin.ModelAdmin):
    list_display = ('discord_id', 'post_date', 'message', 'streak', 'today_problems')
    list_filter = ('post_date',)
    search_fields = ('discord_id',)
    readonly_fields = ('discord_id', 'post_date', 'message', 'streak', 'today_problems')
