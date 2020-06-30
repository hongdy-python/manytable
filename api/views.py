from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from api.models import Book
from .serializers import BookModelSerializerV2


class BookAPIViewV2(APIView):

    def get(self, request, *args, **kwargs):
        book_id = kwargs.get("id")
        print(book_id)
        if book_id:
            book_obj = Book.objects.filter(pk=book_id, is_delete=False).first()
            book_ser = BookModelSerializerV2(book_obj).data
            print(123)
            return Response({
                "status": status.HTTP_200_OK,
                "message": "查询单个图书成功",
                "results": book_ser
            })
        else:
            book_list = Book.objects.filter(is_delete=False)
            book_list_ser = BookModelSerializerV2(book_list, many=True).data
            return Response({
                "status": status.HTTP_200_OK,
                "message": "查询所有图书成功",
                "results": book_list_ser
            })

    def post(self, request, *args, **kwargs):
        request_data = request.data
        if isinstance(request_data, dict):  # 代表增加的是单个图书
            many = False
        elif isinstance(request_data, list):  # 代表添加多个图书
            many = True
        else:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "请求参数格式有误",
            })
        book_ser = BookModelSerializerV2(data=request_data, many=many)
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()
        return Response({
            "status": status.HTTP_200_OK,
            "message": "添加图书成功",
            "result": BookModelSerializerV2(book_obj, many=many).data
        })

    def delete(self, request, *args, **kwargs):
        book_id = kwargs.get("id")
        if book_id:
            ids = [book_id]
        else:
            ids = request.data.get("ids")
        response = Book.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        if response:
            return Response({
                "status": status.HTTP_200_OK,
                "message": "删除成功"
            })
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "删除失败或图书不存在"
        })

    def put(self, request, *args, **kwargs):
        request_data = request.data
        book_id = kwargs.get("id")
        try:
            book_obj = Book.objects.get(pk=book_id)
        except:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "图书不存在"
            })
        # 修改 需要指定instance参数  指定你要修改的是哪一个实例
        book_ser = BookModelSerializerV2(data=request_data, instance=book_obj, partial=False)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "更新成功",
            "results": BookModelSerializerV2(book_obj).data
        })

    def patch(self, request, *args, **kwargs):
        request_data = request.data
        book_id = kwargs.get("id")
        try:
            book_obj = Book.objects.get(pk=book_id)
        except:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "图书不存在"
            })
        #修改 需要指定instance参数
        #修改局部需要指定 partial=True 代表可以修改局部字段
        book_ser = BookModelSerializerV2(data=request_data, instance=book_obj, partial=True)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "更新成功",
            "results": BookModelSerializerV2(book_obj).data
        })