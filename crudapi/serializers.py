from rest_framework import serializers
from .models import Student 

# for inbild user - django provide inbuild user model
from django.contrib.auth.models import User

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'roll', 'city']

    def validate(self, data):
        if data['roll'] > 50:
            raise serializers.ValidationError({'error' : "roll no cannot be greater than 50"})

        if data['name']:
            for n in data['name']:
                if n.isdigit():
                    raise serializers.ValidationError({'error' : "name can not be numeric"})