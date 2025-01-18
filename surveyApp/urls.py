from django.urls import path
from surveyApp import views
app_name = "survey"
urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('create_survey/',views.SurveyCreateView.as_view(), name="create-survey"),
    path('add_questions/<uuid:uid>/',views.create_question, name="add-questions"),
    path('survey/<uuid:uid>/response/', views.SurveyResponseView.as_view(), name='survey_response'),
    path('survey/<uuid:uid>/thank-you/', views.thank_you, name='thank_you'),
]