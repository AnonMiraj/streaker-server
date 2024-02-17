
from django.db import models
from django.utils import timezone


class Trainee(models.Model):
    discord_id = models.CharField(primary_key=True, max_length=50)
    discord_pfp = models.URLField(max_length=550)
    discord_name = models.CharField(max_length=50)
    last_activity = models.DateTimeField(default=timezone.now)

    total_days = models.PositiveIntegerField(default=0)
    total_problems = models.PositiveIntegerField(default=0)
    highest_streak = models.PositiveIntegerField(default=0)
    current_streak = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'trainee'

    def update_streaks(self, new_streak):
        if new_streak > self.highest_streak:
            self.highest_streak = new_streak
        self.current_streak = new_streak

    def __str__(self):
        return self.discord_name


class TraineeRecord(models.Model):
    discord_id = models.CharField(max_length=50)
    post_date = models.DateTimeField(default=timezone.now)
    message = models.TextField(max_length=550)
    streak = models.PositiveIntegerField(default=0)
    today_problems = models.PositiveIntegerField(default=0)

    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE, related_name='trainee_records')

    class Meta:
        db_table = 'trainee_records'
        unique_together = ['discord_id', 'post_date']

    def save(self, *args, **kwargs):
        if not self.pk:
            new_streak = self.streak

            self.trainee.update_streaks(new_streak)
            self.trainee.total_days += 1
            self.trainee.total_problems += self.today_problems
            self.trainee.last_activity = self.post_date

        else:
            old_record = TraineeRecord.objects.get(pk=self.pk)
            self.trainee.total_problems += self.today_problems - old_record.today_problems

        self.trainee.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.trainee.discord_name}: {self.post_date.strftime('%Y-%m-%d')}"
