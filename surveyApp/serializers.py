from rest_framework import serializers
from .models import Survey, Question, Choice, Answer, Response

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['text', 'uid']


class QuestionSerializer(serializers.ModelSerializer):
    # choice_set = serializers.SerializerMethodField()  # Lecture des choix liés
    choices = serializers.JSONField(write_only=True, required=False)  # Champ JSON pour les choix

    class Meta:
        model = Question
        fields = ['survey', 'text', 'type', 'uid', 'choice_set', 'choices']
        read_only_fields = ['uid']
        

    def get_choice_set(self, obj):
        if obj.type in ['single', 'multiple']:
            choices = obj.choice_set.all()
            return ChoiceSerializer(choices, many=True).data
        return []

    def create(self, validated_data):
        choices_data = validated_data.pop('choices', [])
        choice_set = validated_data.pop("choice_set",None)# je fais çça pour eviter le typeError(si je tente de créer Question avec choice_set dans le validated_data, alors que le model Question n'a pas ce champ, ça va lever une exception) 
        question = Question.objects.create(**validated_data)
        #ici la creation des des choix si c'est le type de la quetion n'est pas un text simple
        if question.type in ['single', 'multiple']:
            for choice_text in choices_data:
                Choice.objects.create(text=choice_text, question=question)

        return question

    def update(self, instance, validated_data):
        choices_data = validated_data.pop('choices', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if instance.type in ['single', 'multiple']:
            instance.choice_set.all().delete()
            for choice_text in choices_data:
                Choice.objects.create(text=choice_text, question=instance)

        return instance


class SurveySerializer(serializers.ModelSerializer):
    question_set = QuestionSerializer(many=True)  # Inclut les questions liées

    class Meta:
        model = Survey
        fields = ['uid', 'title', 'description', 'question_set']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['uid', 'response', 'question', 'choice', 'text']


    
class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = '__all__'