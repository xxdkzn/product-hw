from rest_framework import serializers
from .models import StockProduct, Product, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = '__all__'

    def create(self, validated_data):
        positions_data = validated_data.pop('positions')
        stock = Stock.objects.create(**validated_data)
        for position_data in positions_data:
            StockProduct.objects.create(stock=stock, **position_data)
        return stock

    def update(self, instance, validated_data):
        positions_data = validated_data.pop('positions', None)
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        if positions_data:
            # Обновление или создание позиций
            for position_data in positions_data:
                position_id = position_data.get('id')
                if position_id:
                    position = StockProduct.objects.get(id=position_id, stock=instance)
                    position.quantity = position_data.get('quantity', position.quantity)
                    position.price = position_data.get('price', position.price)
                    position.save()
                else:
                    StockProduct.objects.create(stock=instance, **position_data)

        return instance