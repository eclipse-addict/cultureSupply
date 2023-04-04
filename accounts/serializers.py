from .models import User, UserInfo
from rest_framework import serializers
from django.utils import timezone
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailConfirmationHMAC
from allauth.account.utils import send_email_confirmation
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.models import EmailConfirmation, EmailAddress


from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import PasswordResetSerializer
from rest_framework import serializers

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, request):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password1')
        user = User.objects.create_user(email=email, password=password)
        email_address = EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=False)
        email_address.save()
        email_confirmation = EmailConfirmation.create(email_address)
        email_confirmation.sent = timezone.now()
        email_confirmation.save()
        send_email_confirmation(request, user, email=user.email)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user
    
class UserInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserInfo
        fields = '__all__'
        read_only_fields = ( 'user',)