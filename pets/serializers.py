from rest_framework import serializers

from groups.serializers import GroupSerializer

from traits.serializers import TraitSerializer

from .models import Gender


class PetSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=10)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=Gender.choices, default=Gender.DEFAULT)

    group = GroupSerializer()

    traits = TraitSerializer(many=True)
