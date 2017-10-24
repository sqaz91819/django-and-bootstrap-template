from django.db import models

# Create your models here.


class Query(models.Model):
    query = models.CharField(max_length=80, primary_key=True)

    def is_valid(self):
        if self.query['search']:
            return True
        else:
            return False

    def __str__(self):
        return self.query


class ScoreMovie(models.Model):
    score = models.IntegerField(default=1)
    movie = models.CharField(max_length=80, primary_key=True)

    def is_valid(self):
        if self.score['score2'] and self.score['movie2']:
            return True
        else:
            return False

    def __str__(self):
        return self.movie


class Score(models.Model):
    id1 = models.CharField(max_length=40, primary_key=True)
    score = models.IntegerField()

    def is_valid(self):
        if self.id1['id1'] and self.id1['score1']:
            return True
        else:
            return False

    def __str__(self):
        return self.id1
