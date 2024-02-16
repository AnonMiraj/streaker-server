from django.db import models
from django.utils import timezone


class Trainees(models.Model):
    discord_id = models.TextField(primary_key=True, max_length=30)
    discord_pfp = models.TextField(max_length=150)
    discord_name = models.TextField(max_length=30)
    last_activity = models.DateTimeField(default=timezone.now)

    total_days = models.PositiveIntegerField(default=0)
    total_problems = models.PositiveIntegerField(default=0)
    highest_streak = models.PositiveIntegerField(default=0)
    current_streak = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'trainees'

    def update_streaks(self, new_streak):
        if new_streak > self.highest_streak:
            self.highest_streak = new_streak
        self.current_streak = new_streak

    def __str__(self):
        return self.discord_name


class TraineeRecords(models.Model):
    discord_id = models.TextField(max_length=30)
    post_date = models.DateTimeField(default=timezone.now)
    message = models.TextField(max_length=150)
    streak = models.PositiveIntegerField(default=0)
    today_problems = models.PositiveIntegerField(default=0)

    trainee = models.ForeignKey(Trainees, on_delete=models.CASCADE, related_name='trainee_records')

    class Meta:
        db_table = 'trainee_records'

    def save(self, *args, **kwargs):
        if not self.pk:
            new_streak = self.streak

            self.trainee.update_streaks(new_streak)
            self.trainee.total_days += 1
            self.trainee.total_problems += self.today_problems
            self.trainee.last_activity = self.post_date
            self.trainee.save()
        else:
            old_record = TraineeRecords.objects.get(pk=self.pk)
            self.trainee.total_problems += self.today_problems - old_record.today_problems

        self.trainee.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.trainee.discord_name
