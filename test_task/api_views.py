from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from .models import Link, Collection
from .serializers import LinkSerializer, CollectionSerializer, UserSerializer


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['username', 'password']
    ),
    responses={200: 'Token'}
)
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    @swagger_auto_schema(
        operation_description="Register a new user",
        request_body=UserSerializer,
        responses={201: UserSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Get current user profile",
        responses={200: UserSerializer()}
    )
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Update current user profile",
        request_body=UserSerializer,
        responses={200: UserSerializer()}
    )
    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Change password",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['old_password', 'new_password']
        ),
        responses={
            200: "Password changed successfully",
            400: "Invalid password"
        }
    )
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password changed successfully'})


class LinkViewSet(viewsets.ModelViewSet):
    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Get all links for the authenticated user",
        responses={200: LinkSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new link",
        request_body=LinkSerializer,
        responses={201: LinkSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class CollectionViewSet(viewsets.ModelViewSet):
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Collection.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Add a link to a collection",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'link_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the link to add')
            },
            required=['link_id']
        ),
        responses={
            200: CollectionSerializer(),
            400: "Bad Request",
            404: "Not Found"
        }
    )
    @action(detail=True, methods=['post'])
    def add_link(self, request, pk=None):
        collection = self.get_object()
        try:
            link_id = request.data.get('link_id')
            link = Link.objects.get(id=link_id, user=request.user)
            collection.links.add(link)
            return Response(CollectionSerializer(collection).data)
        except Link.DoesNotExist:
            return Response({"error": "Link not found"}, status=404)

    @swagger_auto_schema(
        operation_description="Remove a link from a collection",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'link_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the link to remove')
            },
            required=['link_id']
        ),
        responses={
            200: CollectionSerializer(),
            400: "Bad Request",
            404: "Not Found"
        }
    )
    @action(detail=True, methods=['post'])
    def remove_link(self, request, pk=None):
        collection = self.get_object()
        try:
            link_id = request.data.get('link_id')
            link = Link.objects.get(id=link_id, user=request.user)
            collection.links.remove(link)
            return Response(CollectionSerializer(collection).data)
        except Link.DoesNotExist:
            return Response({"error": "Link not found"}, status=404)
