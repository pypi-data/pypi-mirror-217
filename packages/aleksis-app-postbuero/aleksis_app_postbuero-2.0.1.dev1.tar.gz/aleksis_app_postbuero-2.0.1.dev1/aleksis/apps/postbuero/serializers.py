from rest_framework import serializers

from .models import MailAddress


class MailAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailAddress
        fields = ["username", "address"]

    address = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    def get_address(self, obj):
        return str(obj)

    def get_username(self, obj):
        return obj.person.user.username
