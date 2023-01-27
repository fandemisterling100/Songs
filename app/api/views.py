from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from app.api.serializers import UserLoginSerializer, UserRegisterSerializer, SongSerializer
from django.contrib.auth import get_user_model
from app.users.authentication import UserIsAuthenticated
from app.api.pagination import SongsSetPagination
from app.api.models import Song
from app.api.random_number import RandomNumberConnector

User = get_user_model()


class UserRegisterApiView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer
    model = User


class UserLoginView(TokenObtainPairView):
    def get_serializer_class(self):
        return UserLoginSerializer

class SongCreateAPIView(generics.CreateAPIView):
    permission_classes = [UserIsAuthenticated]
    serializer_class = SongSerializer
    
    def create(self, request, *args, **kwargs):
        self.data = request.data
        # Get current user
        current_user = request.user
        self.data.update({"created_by": current_user.pk})
        serializer = self.get_serializer(data=self.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = {"Song created": serializer.data}
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    
class SongUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [UserIsAuthenticated]
    serializer_class = SongSerializer
    queryset = Song.objects.all()
    
    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            song = get_object_or_404(Song, pk=self.kwargs.get("pk"))
            current_user = request.user
            if song.created_by != current_user:
                return Response({'Permission denied': 'This song is private, you can not update it.'}, status=status.HTTP_400_BAD_REQUEST)
            data = serializer.validated_data
            serializer.update(song, data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SongDeleteApiView(generics.DestroyAPIView):
    permission_classes = [UserIsAuthenticated]
    serializer_class = SongSerializer
    queryset = Song.objects.all()
    
    def delete(self, request, *args, **kwargs):
        song = get_object_or_404(Song, pk=self.kwargs.get("pk"))
        current_user = request.user
        if song.created_by != current_user:
            return Response({'Permission denied': 'This song is private, you can not delete it.'}, status=status.HTTP_400_BAD_REQUEST)
        return self.destroy(request, *args, **kwargs)
    
class SongListAPIView(generics.ListAPIView):
    permission_classes = [UserIsAuthenticated]
    serializer_class = SongSerializer
    pagination_class = SongsSetPagination

    def get_queryset(self):
        user = self.request.user
        return Song.objects.filter(created_by=user)
    
class PublicSongsListAPIView(generics.ListAPIView):
    permission_classes = [UserIsAuthenticated]
    serializer_class = SongSerializer
    pagination_class = SongsSetPagination
    queryset = Song.objects.filter(private=False)
    
    
class SongRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [UserIsAuthenticated]
    serializer_class = SongSerializer
    queryset = Song.objects.all()
    
    def get(self, request, *args, **kwargs):
        song = get_object_or_404(Song, pk=self.kwargs.get("pk"))
        current_user = request.user
        if song.created_by != current_user and song.private:
            return Response({'Permission denied': 'This song is private, you can not retrieve it.'}, status=status.HTTP_400_BAD_REQUEST)
        return self.retrieve(request, *args, **kwargs)
    

class GenerateRandomNumberAPIView(APIView):
    permission_classes = [UserIsAuthenticated]

    def get(self, request, format=None):
        connector = RandomNumberConnector()
        number = connector.get_number()

        return Response(
            {
                "Random number generated": number
            },
            status=status.HTTP_200_OK,
        )