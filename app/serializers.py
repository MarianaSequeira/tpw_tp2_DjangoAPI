from app.models import *
from rest_framework import  serializers

class ReceitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receita
        fields = ('nome', 'descricao', 'tipo', 'preparacao', 'tempo', 'tempo', 'dificuldade', 'dose', 'data', 'utilizador', 'classificacao')


class IngredientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredientes
        fields = ('ingredienteName', 'ingredienteQuant', 'unidade')


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('nome')


class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredientes
        fields = ('comentario', 'data', 'utilizador')

