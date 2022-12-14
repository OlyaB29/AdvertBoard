from django.db.models import OuterRef, Subquery
from rest_framework import generics, permissions
from .models import Advert, Gallery, Photo, Category, Region, Value, Chat, Message
from .serializers import AdvertListSerializer, AdvertDetailSerializer, CategoryListSerializer, RegionSerializer, \
    ValueSerializer, AdvertUpdateSerializer, PhotoSerializer, AdvertCreateSerializer, ChatSerializer, \
    ChatCreateSerializer, MessageSerializer, MessageCreateSerializer
from django.contrib.auth.models import User


class AdvertListView(generics.ListAPIView):
    # Вывод списка объявлений
    permission_classes = [permissions.AllowAny]
    serializer_class = AdvertListSerializer

    def get_queryset(self):
        photo = Photo.objects.filter(gallery__advert=OuterRef("pk"))
        adverts = Advert.objects.filter(moderation=True).annotate(main_photo=Subquery(photo.values('image')[:1]))
        return adverts


class AdvertDetailView(generics.RetrieveAPIView):
    # Вывод подробной информации об объявлении
    queryset = Advert.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = AdvertDetailSerializer
    lookup_field = 'id'


class AdvertCreateView(generics.CreateAPIView):
    # Добавление объявления
    permission_classes = [permissions.IsAuthenticated]
    queryset = Advert.objects.all()
    serializer_class = AdvertCreateSerializer


class UserAdvertListView(generics.ListAPIView):
    # Все объявления пользователя
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AdvertListSerializer

    def get_queryset(self):
        photo = Photo.objects.filter(gallery__advert=OuterRef("pk"))
        adverts = Advert.objects.filter(user=self.request.user).annotate(main_photo=Subquery(photo.values('image')[:1]))
        return adverts


class UserAdvertUpdateView(generics.RetrieveUpdateAPIView):
    # Редактирование объявления пользователя
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AdvertUpdateSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Advert.objects.filter(user=self.request.user)


class UserAdvertDeleteView(generics.DestroyAPIView):
    # Удаление объявления пользователя
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Advert.objects.filter(user=self.request.user)


# id=self.kwargs.get("pk"),
class CategoryListView(generics.ListAPIView):
    # Вывод списка категорий
    permission_classes = [permissions.AllowAny]
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()


class RegionListView(generics.ListAPIView):
    # Вывод списка регионов
    permission_classes = [permissions.AllowAny]
    serializer_class = RegionSerializer
    queryset = Region.objects.all()


class ValueListView(generics.ListAPIView):
    # Вывод списка значений характеристик
    permission_classes = [permissions.AllowAny]
    serializer_class = ValueSerializer
    queryset = Value.objects.all()


class PhotoCreateView(generics.ListCreateAPIView):
    # Добавление фото
    permission_classes = [permissions.IsAuthenticated]
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class PhotoUpdateView(generics.RetrieveUpdateAPIView):
    # Редактирование фотографии
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PhotoSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Photo.objects.filter(gallery__advert__user=self.request.user)


class PhotoDeleteView(generics.DestroyAPIView):
    # Удаление фотографии
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Photo.objects.filter(gallery__advert__user=self.request.user)


class UserChatListView(generics.ListAPIView):
    # Вывод списка бесед пользователя
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatSerializer

    def get_queryset(self):
        message = Message.objects.filter(chat=OuterRef("pk")).order_by('-pub_date')
        chats = (Chat.objects.filter(buyer=self.request.user) | Chat.objects.filter(seller=self.request.user)).annotate(
            last_message_date=Subquery(message.values('pub_date')[:1]), last_message_text=Subquery(message.values('text')[:1]))
        chats = chats.order_by('-last_message_date')
        return chats


class ChatCreateView(generics.CreateAPIView):
    # Создание беседы
    permission_classes = [permissions.IsAuthenticated]
    queryset = Chat.objects.all()
    serializer_class = ChatCreateSerializer


class ChatDeleteView(generics.DestroyAPIView):
    # Удаление беседы пользователя
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        chats = Chat.objects.filter(buyer=self.request.user) | Chat.objects.filter(seller=self.request.user)
        return chats


class MessageListView(generics.ListAPIView):
    # Вывод списка сообщений чата
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        messages = Message.objects.filter(chat__id=self.kwargs['chat_id'])
        messages.filter(is_readed=False).exclude(author=self.request.user).update(is_readed=True)
        return messages


class MessageCreateView(generics.CreateAPIView):
    # Создание сообщения
    permission_classes = [permissions.IsAuthenticated]
    queryset = Message.objects.all()
    serializer_class = MessageCreateSerializer
