from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.serializers import *
from datetime import datetime

@api_view(['GET'])
def get_receita(request):
    id = int(request.GET['id'])
    try:
        receita = Receita.objects.get(id=id)
    except Receita.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ReceitaSerializer(receita)
    return Response(serializer.data)


@api_view(['GET'])
def get_receita_tipo(request):
    tipo = request.GET['tipo']
    if tipo == 'like':
        receitas = Receita.objects.order_by("-classificacao")[0:6]
    else:
        receitas = receitas = Receita.objects.filter(tipo=tipo)
    serializer = ReceitaSerializer(receitas, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def save_receita(request):
    serializer = ReceitaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_receita(request, id):
    try:
        receita = Receita.objects.get(id=id)
    except Receita.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    receita.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_receitas(request):
    receitas = Receita.objects.all()
    serializer = ReceitaSerializer(receitas, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_tags_receita(request):
    idReceita = request.POST(['id'])
    receita = Receita.objects.get(id=idReceita)
    tags = [tag for tag in Tags.objects.all() if receita in tag.receitas.all()]
    serializer = TagsSerializer(tags, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_receitas_tag(request):
    nome_tag = request.POST['tag']
    tag = Tags.objects.get(nome=nome_tag)
    receitas = tag.receitas.all()
    serializer = ReceitaSerializer(receitas, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_receitas_utilizador(request):
    utilizador = request.GET['utilizador']
    receitas = Receita.objects.filter(utilizador=utilizador)
    serializer = ReceitaSerializer(receitas, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_receitas_guardadas(request):
    utilizador = request.GET['utilizador']
    receitasGuardadas = ReceitasGuardadas.objects.filter(utilizador=utilizador)
    receitas = [receita.receita for receita in receitasGuardadas]
    serializer = ReceitaSerializer(receitas, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def comentar_receita(request):
    id_receita = request.POST['id_receita']
    utilizador = request.POST['utilizador']
    comentario = request.POST['comentario']
    receita = Receita.objects.get(id=id_receita)
    c = Comentario(receita=receita, data=datetime.now().strftime('%Y-%m-%d'), utilizador=utilizador,
                   comentario=comentario)
    c.save()
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def pesquisar(request):
    if 'query' in request.POST:
        query = request.POST['query']
        queryResult = Receita.objects.filter(nome__contains=query)
    if 'tags' in request.POST and len(request.POST.getlist('tags', [])) > 1:
        lst_tags = request.POST.getlist('tags', [])
        temp_receitas = []
        for t in lst_tags:
            if t == '':
                continue
            tag = Tags.objects.get(nome=t)
            tag_receitas = tag.receitas.all()
            for r in queryResult:
                if r in tag_receitas:
                    temp_receitas.append(r)

        queryResult = temp_receitas
    serializer = ReceitaSerializer(queryResult, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def receitas_gostadas(request):
    utilizador = request.GET['utilizador']
    receitas_gostadas = ReceitasGostadas.objects.filter(utilizador=utilizador)
    receitas = [receitas_gostada.receita for receitas_gostada in receitas_gostadas]
    serializer = ReceitaSerializer(receitas, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def ingredientes_receita(request):
    id = request.GET['id']
    receita = Receita.objects.get(id=id)
    lst_ingredientes = Ingredientes.objects.filter(receita=receita)
    serializer = IngredientesSerializer(lst_ingredientes, many=True)
    return Response(serializer.data)




