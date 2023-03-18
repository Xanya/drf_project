from django.http import JsonResponse
from django.forms.models import model_to_dict

from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer

import json

""" @api_view(['GET'])
def api_home(request, *args, **kwargs):
    instance = Product.objects.order_by("?").first()
    if instance:
        data = ProductSerializer(instance).data
    return Response(data) """

@api_view(['POST'])
def api_home(request, *args, **kwargs):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        #instance = serializer.save()
        #print(instance)
        print(serializer.data)
        return Response(serializer.data)