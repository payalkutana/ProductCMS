from rest_framework import serializers
from .models import product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = ['name','image','price']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance