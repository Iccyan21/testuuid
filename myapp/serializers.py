from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        
    def to_representation(self, instance):
        request = self.context.get('request')
        if request:
            request_user = request.user
            # `instance.userid` を `instance.account.userid` に変更
            if not instance.is_public and instance.account.userid != request_user:
                raise serializers.ValidationError('You do not have permission to view this post.')
        return super().to_representation(instance)

from rest_framework import serializers
from .models import Account

class AccountLoginSerializer(serializers.Serializer):
    userid = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = Account.objects.get(userid=data['userid'])
            if user.password != data['password']:
                raise serializers.ValidationError("Incorrect password.")
        except Account.DoesNotExist:
            raise serializers.ValidationError("User not found.")
        return data