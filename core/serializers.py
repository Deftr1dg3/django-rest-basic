from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer 
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

class UserCreateSerializer(BaseUserCreateSerializer):
    
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']
        # Very bad approach - Spagetti Pattern
        # If you want to define field, that is not in User table
        # for example birth_date
        # fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'birth_date']
        # you need to explicitly define it.
        
    # birth_date = serializers.DateField() 
    
        
    
    
class UserSerializer(BaseUserSerializer):
    
    class Meta(BaseUserSerializer.Meta):

        fields = ['id', 'username', 'email', 'first_name', 'last_name']