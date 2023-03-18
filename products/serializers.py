from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Product
from . import validators
from api.serializers import UserPublicSerializer

class ProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name='product-detail', lookup_field = 'pk', read_only=True)
    title = serializers.CharField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    #related_products = ProductInlineSerializer(source='user.product_set.all', read_only=True, many=True)
    my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='product-detail', lookup_field = 'pk')
    title = serializers.CharField(validators=[validators.validate_title_no_hello, validators.unique_title_validator])
    user = UserPublicSerializer(read_only=True)
    body = serializers.CharField(source='content')
    #user_data = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = [
            'user',
            #'user_data',
            'url',
            'edit_url',
            'pk',
            'title',
            'body',
            'price',
            'sale_price',
            'my_discount',
            'public',
            'path',
            'endpoint'
            #'related_products'
        ]

    def get_user_data(self, obj):
        return {
            'username': obj.user.username
        }

    # def validate_title(self, value):
    #     qs = Product.objects.filter(title__iexact=value)
    #     if qs.exists():
    #         raise serializers.ValidationError(f'{value} already exists!')
    #     return value

    # def create(self, validated_data):
    #     email = validated_data.pop('email')
    #     title = validated_data.get('title')
    #     content = validated_data.get('content') or None
    #     if content is None:
    #         validated_data.pop('content')
    #         print(email, content)
    #         return Product.objects.create(content=title, **validated_data)
    #     print(email, content)
    #     return super().create(validated_data)
    
    # def update(self, instance, validated_data):
    #     email = validated_data.pop('email')
    #     return super().update(instance, validated_data)
    
    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse('product-update', kwargs={'pk': obj.pk}, request=request)
    
    def get_my_discount(self, obj):
        if not hasattr(obj, 'id'):
            return None
        return obj.get_discount()
    
class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'title',
            'price'
        ]