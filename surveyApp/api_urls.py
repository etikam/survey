from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    SurveyViewSet, 
    QuestionViewSet, 
    ChoiceViewSet, 
    ResponseViewSet, 
    AnswerViewSet
)

router = DefaultRouter()
router.register(r'surveys', SurveyViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'choices', ChoiceViewSet)
router.register(r'responses', ResponseViewSet)
router.register(r'answers', AnswerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
