from app.models import *
from rest_framework import  serializers

class ReceitaSerializer(serializers.ModelSerializer):
    imagem = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = Receita
        fields = ('id', 'nome', 'descricao', 'tipo', 'preparacao', 'tempo', 'tempo', 'dificuldade', 'dose', 'data', 'utilizador', 'classificacao', 'imagem')


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

