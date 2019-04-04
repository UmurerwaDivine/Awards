from rest_framework import serializers
from .models import Pic

class MerchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pic
        fields = ('pic', 'user', 'pic_link','pic_caption', 'pub_date', 'pic_name')