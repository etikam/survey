from rest_framework.mixins import (
    CreateModelMixin, 
    ListModelMixin, 
    RetrieveModelMixin, 
    UpdateModelMixin, 
    DestroyModelMixin
)
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Survey, Question, Choice, Answer, Response
from .serializers import (
    SurveySerializer,
    QuestionSerializer,
    AnswerSerializer,
    ResponseSerializer,
    ChoiceSerializer
)
from .filters import (
    SurveyFilterSet, 
    QuestionFilterSet, 
    ChoiceFilterSet, 
    ResponseFilterSet, 
    AnswerFilterSet
)

# Survey ViewSet with full CRUD and additional actions
class SurveyViewSet(ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SurveyFilterSet

    @action(detail=True, methods=["get"])
    def questions(self, request, pk=None):
        """Récupérer les questions associées à un sondage"""
        survey = get_object_or_404(Survey, pk=pk)
        questions = survey.question_set.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def responses(self, request, pk=None):
        """Récupérer les réponses pour un sondage"""
        survey = get_object_or_404(Survey, pk=pk)
        responses = survey.response_set.all()
        serializer = ResponseSerializer(responses, many=True)
        return Response(serializer.data)

# Question ViewSet with full CRUD and additional actions
class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all().order_by("-created_at")
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = QuestionFilterSet

    @action(detail=True, methods=["get"])
    def choices(self, request, pk=None):
        """Récupérer les choix pour une question"""
        question = get_object_or_404(Question, pk=pk)
        choices = question.choice_set.all()
        serializer = ChoiceSerializer(choices, many=True)
        return Response(serializer.data)

# Choice ViewSet with full CRUD
class ChoiceViewSet(ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ChoiceFilterSet

# Response ViewSet with full CRUD and additional actions
class ResponseViewSet(ModelViewSet):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ResponseFilterSet

    def perform_create(self, serializer):
        """Assigner automatiquement l'utilisateur à la réponse"""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["get"])
    def answers(self, request, pk=None):
        """Récupérer les réponses associées à une réponse principale"""
        response = get_object_or_404(Response, pk=pk)
        answers = response.answer_set.all()
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)

# Answer ViewSet with full CRUD
class AnswerViewSet(ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AnswerFilterSet
