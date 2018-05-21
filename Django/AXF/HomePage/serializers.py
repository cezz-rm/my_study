from rest_framework import serializers

from HomePage.models import CartModel, Goods


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartModel
        fields = ['id', 'c_num', 'is_select', 'goods', 'user']

        # 显示外键的所有字段
        # depth = 1
        # 除了某个字段其他的都显示
        # exclude = ['c_num']

    # def to_representation(self, instance):
    #     pass


class allGoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        exclude = ['id']
