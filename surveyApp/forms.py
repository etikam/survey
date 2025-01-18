from django import forms
from .models import Survey
from .models import Question
from .models import Choice
from .models import Answer
from django.utils import timezone


class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ["image","title", "description", "start_date", "end_date"]
        widgets = {
            "image": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Titre du sondage"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Description du sondage",
                    "rows": 3,
                }
            ),
            "start_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "end_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError(
                    "La date de fin doit être postérieure à la date de début."
                )
            if start_date < timezone.now():
                raise forms.ValidationError(
                    "La date de début ne peut pas être dans le passé."
                )


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text", "type"]
        widgets = {
            "text": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Texte de la question"}
            ),
            "type": forms.Select(attrs={"class": "form-control"}),
        }


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Texte du choix'}),
        }
        


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        exclude = ['response', 'question', 'choice', 'text']
        fields = []

    def __init__(self, *args, **kwargs):
        survey = kwargs.pop('survey')  # Récupérer le sondage
        super().__init__(*args, **kwargs)

        for question in survey.question_set.all():
            if question.type == "text":
                self.fields[f"question_{question.uid}"] = forms.CharField(
                    label=question.text, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
            elif question.type == "multiple":
                # Créer un champ MultipleChoiceField pour gérer les checkbox
                choices = [(choice.uid, choice.text) for choice in question.choice_set.all()]
                self.fields[f"question_{question.uid}"] = forms.MultipleChoiceField(
                    label=question.text, choices=choices, widget=forms.CheckboxSelectMultiple, required=True)
            else:
                choices = [(choice.uid, choice.text) for choice in question.choice_set.all()]
                self.fields[f"question_{question.uid}"] = forms.ChoiceField(
                    label=question.text, choices=choices, widget=forms.RadioSelect, required=True)
