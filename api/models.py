from django.db import models


class Trainees(models.Model):
    discord_id = models.TextField(primary_key=True, max_length=30)
    discord_pfp = models.TextField(max_length=150)
    discord_name = models.TextField(max_length=30)
    total_days = models.IntegerField(default=0)
    total_problems = models.IntegerField(default=0)
    highest_streak = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)

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
    post_date = models.DateTimeField()
    message = models.TextField(max_length=150)
    streak = models.IntegerField(default=0)
    today_problems = models.IntegerField(default=0)

    trainee = models.ForeignKey(Trainees, on_delete=models.CASCADE, related_name='trainee_records')

    class Meta:
        db_table = 'trainee_records'

    def save(self, *args, **kwargs):
        if not self.pk:
            new_streak = self.streak

            self.trainee.update_streaks(new_streak)
            self.trainee.total_days += 1
            self.trainee.total_problems += self.today_problems
            self.trainee.save()
        else:
            old_record = TraineeRecords.objects.get(pk=self.pk)
            old_problems = old_record.today_problems

            self.trainee.total_problems -= old_problems
            self.trainee.total_problems += self.today_problems
            self.trainee.save()
            #
            # subsequent_records = self.trainee.trainee_records.filter(post_date__gt=self.post_date).order_by('post_date')
            # current_streak = self.streak
            #
            # for record in subsequent_records:
            #     if record.streak == current_streak+1:
            #         record.streak -= 1
            #     else:
            #         break
            #     current_streak += 1
            #     record.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.trainee.discord_name
