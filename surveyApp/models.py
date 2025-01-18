import uuid
from django.db import models
from django.contrib.auth.models import User


class Survey(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="survey_images")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)


class Question(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    QUESTION_TYPES = [
        ("single", "Réponse unique"),
        ("multiple", "Réponse multiple"),
        ("text", "Réponse texte"),
    ]
    text = models.CharField(max_length=500)
    type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)


class Choice(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class Response(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
