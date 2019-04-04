from rest_framework import serializers
from .models import Pic

class MerchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pic
        fields = ('user', 'pic_caption', 'pic_link', 'pub_date', ' pic')