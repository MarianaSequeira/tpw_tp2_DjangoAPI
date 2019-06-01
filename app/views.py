from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
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
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def save_receita(request):
    print(request.FILES)
    nome = request.data['nome']
    descricao = request.data['descricao']
    preparacao = request.data['preparacao']
    tipoReceita = request.data['tipoReceita']
    tempo = request.data['tempo']
    nivel = request.data['nivel']
    dose = request.data['dose']
    utilizador = request.data['utilizador']
    imagem = request.data['imagem']
    print(imagem)
    receita = Receita(nome=nome, descricao=descricao, preparacao=preparacao, tipo=tipoReceita, tempo=tempo, dificuldade=nivel, dose=dose, imagem=imagem, data=datetime.now().strftime('%Y-%m-%d'), classificacao=0, utilizador=utilizador)
    receita.save()
    for ingrediente in request.data['ingredientes']:
        nome = ingrediente['ingrediente']
        quantidade = ingrediente['quantidade']
        unidade = ingrediente['unidade']
        new_ingrediente = Ingredientes(receita=receita, ingredienteName=nome, ingredienteQuant=quantidade, unidade=unidade)
        new_ingrediente.save()
    for tag in request.data['tags']:
        t = Tags.objects.get(nome=tag)
        t.receitas.add(receita)
    return Response(status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
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
    idReceita = request.GET['id']
    receita = Receita.objects.get(id=idReceita)
    tags = [tag for tag in Tags.objects.all() if receita in tag.receitas.all()]
    serializer = TagsSerializer(tags, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_receitas_tag(request):
    nome_tag = request.GET['tag']
    tag = Tags.objects.get(nome=nome_tag)
    receitas = tag.receitas.all()
    serializer = ReceitaSerializer(receitas, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def get_receitas_utilizador(request):
    utilizador = request.GET['utilizador']
    receitas = Receita.objects.filter(utilizador=utilizador)
    serializer = ReceitaSerializer(receitas, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def get_receitas_guardadas(request):
    utilizador = request.GET['utilizador']
    receitasGuardadas = ReceitasGuardadas.objects.filter(utilizador=utilizador)
    receitas = [receita.receita for receita in receitasGuardadas]
    serializer = ReceitaSerializer(receitas, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def comentar_receita(request):
    id_receita = request.data['id_receita']
    utilizador = request.data['utilizador']
    comentario = request.data['comentario']
    receita = Receita.objects.get(id=id_receita)
    c = Comentario(receita=receita, data=datetime.now().strftime('%Y-%m-%d'), utilizador=utilizador,
                   comentario=comentario)
    c.save()
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_comentarios_receita(request):
    id_receita = request.GET['id']
    receita = Receita.objects.get(id=id_receita)
    lst_comentarios = Comentario.objects.filter(receita=receita)
    serializer = ComentarioSerializer(lst_comentarios, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def pesquisar(request):
    print(request.GET)
    if 'query' in request.GET:
        query = request.GET['query']
        queryResult = Receita.objects.filter(nome__contains=query)
    if 'tags' in request.GET:
        print('aqui')
        lst_tags = request.GET.getlist('tags', [])
        print(lst_tags)
        temp_receitas = []
        for t in lst_tags:
            if t == '':
                continue
            tag = Tags.objects.get(nome=t)
            tag_receitas = tag.receitas.all()
            for r in queryResult:
                if r in tag_receitas:
                    temp_receitas.append(r)
        print(temp_receitas)
        queryResult = temp_receitas
    serializer = ReceitaSerializer(queryResult, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
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

@api_view(['GET'])
def tags(request):
    tags = Tags.objects.all()
    serializer = TagsSerializer(tags, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def gostar_receita(request):
    id_receita = request.data['id']
    username = request.data['utilizador']
    receita = Receita.objects.get(id=id_receita)

    if ReceitasGostadas.objects.filter(receita=receita, utilizador=username):
        ReceitasGostadas.objects.get(receita=receita, utilizador=username).delete()
        receita.classificacao -= 1
        receita.save()
    else:
        receitaGostada = ReceitasGostadas(receita=receita, utilizador=username)
        receitaGostada.save()
        receita.classificacao += 1
        receita.save()
    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, ))
@permission_classes((IsAuthenticated, ))
def guardar_receita(request):
    id_receita = request.data['id']
    username = request.data['utilizador']
    receita = Receita.objects.get(id=id_receita)

    if ReceitasGuardadas.objects.filter(receita=receita, utilizador=username):
        ReceitasGuardadas.objects.get(receita=receita, utilizador=username).delete()
    else:
        receitaGuardada = ReceitasGuardadas(receita=receita, utilizador=username)
        receitaGuardada.save()
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_extra_info(request):
    id_receita = request.GET['id']
    receita = Receita.objects.get(id=id_receita)

    saved = ReceitasGuardadas.objects.filter(receita=receita, utilizador=request.user)
    liked = ReceitasGostadas.objects.filter(receita=receita, utilizador=request.user)

    if not saved:
        bookclass = "far fa-bookmark"
    else:
        bookclass = "fas fa-bookmark"

    if not liked:
        likeclass = "far fa-heart"
    else:
        likeclass = "fas fa-heart"

    content = {'bookclass': bookclass, 'likeclass': likeclass}
    return Response(content)


@api_view(['POST'])
def sign_up(request):
    print('aqui')
    username = request.data['username']
    password = request.data['password']
    user = User.objects.create(username=username, password=password)
    user.set_password(user.password)
    user.save()
    return Response(status=status.HTTP_201_CREATED)



class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'username': user.username,
            'token': token.key
        })





