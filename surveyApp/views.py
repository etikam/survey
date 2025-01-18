from django.shortcuts import render,get_object_or_404, redirect
from django.urls import reverse
from surveyApp.forms import SurveyForm, AnswerForm, QuestionForm
from django.contrib import messages
from django.views.generic import CreateView, ListView, View
from .models import Survey, Question, Choice, Answer, Response
from django.utils import timezone
# Create your views here.


class HomeView(ListView):
    model = Survey
    template_name = "surveyApp/home/index.html"
    context_object_name = 'surveys'

    def get_context_data(self, **kwargs):
        # Récupérer le contexte de base
        context = super().get_context_data(**kwargs)
        # Ajouter la variable `today` au contexte
        context['today'] = timezone.now()
        return context



class SurveyCreateView(View):
    def get(self, request):
        # Créer le formulaire de sondage et de questions
        survey_form = SurveyForm()
        question_form = QuestionForm()

        return render(request, 'surveyApp/home/survey_create.html', {
            'survey_form': survey_form,
            'question_form': question_form
        })

    def post(self, request):
        # Inclure request.FILES pour gérer les fichiers (comme l'image)
        survey_form = SurveyForm(request.POST, request.FILES)
        question_form = QuestionForm(request.POST)

        # Si le formulaire de sondage est valide
        if survey_form.is_valid():
            # Créer un nouveau sondage
            survey = survey_form.save(commit=False)
            survey.creator = request.user
            survey.save()

            # Gérer les questions et les choix associés
            questions = request.POST.getlist("questions[]")  # Liste des questions
            types = request.POST.getlist("types[]")  # Liste des types de question
            choices_data = request.POST.getlist("choices[]")  # Liste des choix (si applicable)

            for index, text in enumerate(questions):
                question_type = types[index]
                question = Question.objects.create(
                    text=text,
                    type=question_type,
                    survey=survey
                )

                # Si la question est de type "single" ou "multiple", ajouter des choix
                if question_type in ["single", "multiple"]:
                    choices = choices_data[index].split(",")  # Exemple de structure de choix séparée par des virgules
                    for choice_text in choices:
                        Choice.objects.create(text=choice_text.strip(), question=question)

            messages.success(request, "Sondage et questions créés avec succès.")
            return redirect('survey:home')  # Redirection vers la liste des sondages

        # Si l'un des formulaires n'est pas valide, retourner avec des messages d'erreur
        messages.error(request, f"Erreur lors de la création du sondage ou des questions. {survey_form.errors}")
        return render(request, 'surveyApp/home/survey_create.html', {
            'survey_form': survey_form,
            'question_form': question_form
        })
        


def create_question(request, uid):
    survey = get_object_or_404(Survey, uid=uid)
    
    if request.method == "POST":
        questions = request.POST.getlist("questions[]")  # Liste des textes des questions
        types = request.POST.getlist("types[]")  # Liste des types correspondants
        choices_data = request.POST.getlist("choices[]")  # Liste des choix (format JSON ou similaire)

        for index, text in enumerate(questions):
            question_type = types[index]
            question = Question.objects.create(text=text, type=question_type, survey=survey)

            # Gérer les choix si le type est "single" ou "multiple"
            if question_type in ["single", "multiple"]:
                choices = choices_data[index].split(",")  # Exemple de structure de choix séparée par des virgules
                for choice_text in choices:
                    Choice.objects.create(text=choice_text.strip(), question=question)

        messages.success(request, "Les questions ont été ajoutées avec succès.")
        return redirect("survey:home")  # Redirection vers un détail ou liste de sondage

    return render(request, "surveyApp/home/add_question.html", {"survey": survey})



class SurveyResponseView(View):
    # @login_required
    def get(self, request, uid):
        # Récupérer le sondage et vérifier la validité des dates
        survey = get_object_or_404(Survey, uid=uid)
        
        # Créer un formulaire dynamique basé sur les questions du sondage
        form = AnswerForm(survey=survey)
        
        return render(request, 'surveyApp/home/survey_response.html', {'survey': survey, 'form': form})


    def post(self, request, uid):
        survey = get_object_or_404(Survey, uid=uid)
        form = AnswerForm(request.POST, survey=survey)

        if form.is_valid():
            # Créer la réponse principale pour l'utilisateur
            response = Response.objects.create(user=request.user, survey=survey)
            
            for field_name, field_value in form.cleaned_data.items():
                if field_name.startswith('question_'):
                    question_uid = field_name.split('_')[1]
                    question = Question.objects.get(uid=question_uid)
                    
                    # Gérer les réponses texte
                    if question.type == "text":
                        Answer.objects.create(response=response, question=question, text=field_value)
                    
                    # Gérer les réponses à choix (radio, choix unique)
                    elif question.type == "single":
                        choice = Choice.objects.get(uid=field_value)
                        Answer.objects.create(response=response, question=question, choice=choice)
                    
                    # Gérer les réponses avec des cases à cocher (multiple)
                    elif question.type == "multiple":
                        # Si la question a plusieurs réponses (cases à cocher), 
                        # 'field_value' devrait être une liste des UID des choix sélectionnés.
                        for choice_uid in field_value:  # field_value est une liste de choix sélectionnés
                            choice = Choice.objects.get(uid=choice_uid)
                            Answer.objects.create(response=response, question=question, choice=choice)

            messages.success(request, "Vos réponses ont été enregistrées avec succès.")
            return redirect('survey:thank_you', uid=survey.uid)

        return render(request, 'surveyApp/home/survey_response.html', {'survey': survey, 'form': form})


def thank_you(request, uid):
    survey = get_object_or_404(Survey, uid=uid)
    return render(request, 'surveyApp/home/thank_you.html', {'survey': survey})
