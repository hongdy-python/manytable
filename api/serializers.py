from rest_framework import serializers, exceptions

from api.models import Book, Press


class PressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Press
        fields = ("press_name", "address", "pic")


class BookModelSerializerV2(serializers.ModelSerializer):
    class Meta:
        print(564)
        model = Book
        # fields应该填写哪些字段  应该填写序列化与反序列化字段的并集
        print(model,111)
        fields = ("book_name","price", "publish", "authors", "pic")
        print(222)
        # 通过此参数指定哪些字段是参与序列化的  哪些字段是参与反序列化的
        extra_kwargs = {
            "book_name": {
                "required": True,  # 设置为必填字段
                "min_length": 3,  # 最小长度
                "error_messages": {
                    "required": "图书名是必填的",
                    "min_length": "长度不够，太短啦~"
                }
            },
            # 指定此字段只参与反序列化
            "publish": {"write_only": True},
            "authors": {"write_only": True},
            # 指定某个字段只参与序列化
            "pic": {"read_only": True}
        }

    def validate_book_name(self, value):
        # 自定义用户名校验规则
        if "1" in value:
            raise exceptions.ValidationError("图书名含有敏感字")
        return value

    def validate(self, attrs):
        price = attrs.get("price", 0)
        if price > 90:
            raise exceptions.ValidationError("超过设定的最高价钱~")
        return attrs
