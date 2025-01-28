from django_filters import rest_framework as filters
from .models import Survey, Question, Choice, Response, Answer

class SurveyFilterSet(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    start_date = filters.DateTimeFromToRangeFilter()
    end_date = filters.DateTimeFromToRangeFilter()
    creator_username = filters.CharFilter(field_name='creator__username', lookup_expr='icontains')

    class Meta:
        model = Survey
        fields = ['title', 'creator', 'start_date', 'end_date', 'creator_username']

class QuestionFilterSet(filters.FilterSet):
    text = filters.CharFilter(lookup_expr='icontains')
    survey_title = filters.CharFilter(field_name='survey__title', lookup_expr='icontains')
    
    class Meta:
        model = Question
        fields = ['survey', 'type', 'text', 'survey_title']

class ChoiceFilterSet(filters.FilterSet):
    text = filters.CharFilter(lookup_expr='icontains')
    question_text = filters.CharFilter(field_name='question__text', lookup_expr='icontains')

    class Meta:
        model = Choice
        fields = ['question', 'text', 'question_text']

class ResponseFilterSet(filters.FilterSet):
    survey_title = filters.CharFilter(field_name='survey__title', lookup_expr='icontains')
    user_username = filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    created_at = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Response
        fields = ['survey', 'user', 'created_at', 'survey_title', 'user_username']

class AnswerFilterSet(filters.FilterSet):
    response_survey = filters.CharFilter(field_name='response__survey__title', lookup_expr='icontains')
    question_text = filters.CharFilter(field_name='question__text', lookup_expr='icontains')
    choice_text = filters.CharFilter(field_name='choice__text', lookup_expr='icontains')

    class Meta:
        model = Answer
        fields = ['response', 'question', 'choice', 'text', 'response_survey', 'question_text', 'choice_text']