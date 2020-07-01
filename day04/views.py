from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework import generics
from rest_framework import viewsets

from api.models import Book
from utils.response import APIResponse
from .serializers import BookModelSerializer


class BookAPIView(APIView):

    def get(self, request, *args, **kwargs):
        book_list = Book.objects.filter(is_delete=False)
        data_ser = BookModelSerializer(book_list, many=True).data

        return APIResponse(results=data_ser)


# GenericAPIView继承了APIView, 两者完全兼容
class BookGenericAPIView(ListModelMixin,
                         RetrieveModelMixin,
                         CreateModelMixin,
                         UpdateModelMixin,
                         DestroyModelMixin,
                         GenericAPIView):
    # 获取当前视图所操作的模型 与序列化器类
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    # 指定获取单条信息的主键的名称
    lookup_field = "id"


    # 通过继承RetrieveModelMixin 提供了self.retrieve 完成了查询单个
    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            return self.retrieve(request, *args, **kwargs)
        # 通过继承ListModelMixin 提供self.list完成了查询所有
        else:
            return self.list(request, *args, **kwargs)

    # 新增图书  通过继承CreateModelMixin 来获得self.create方法  内部完成了新增
    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        return APIResponse(results=response.data)

    # 单整体改
    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return APIResponse(results=response.data)

    # 单局部改
    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        return APIResponse(results=response.data)

    # 通过继承DestroyModelMixin 获取self
    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return APIResponse(http_status=status.HTTP_204_NO_CONTENT)


class BookListAPIVIew(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "id"


class BookGenericViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "id"

    # 如何确定post请求是需要登录
    def user_login(self, request, *args, **kwargs):
        request_data = request.data
        book_names = Book.objects.all().values("book_name")
        for bookname in book_names:
            if bookname.get("book_name") == request_data.get("book_name"):
                return APIResponse(data_status=200,data_message="登陆成功")
            else:
                return APIResponse(data_status=400,data_message="登陆失败")

    def user_register(self, request, *args, **kwargs):
        request_data = request.data
        book_names = Book.objects.all().values("book_name")
        for bookname in book_names:
            if bookname.get("book_name") == request_data.get("book_name"):
                return APIResponse(data_status=400, data_message="注册失败")
        BookGenericAPIView.post(self,request,*args,**kwargs)
        return APIResponse(data_status=200, data_message="注册成功")


