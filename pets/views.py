from django.shortcuts import render

from rest_framework.views import APIView, Request, Response, status

from rest_framework.pagination import PageNumberPagination

from .models import Pet

from groups.models import Group

from traits.models import Trait

from .serializers import PetSerializer


class PetView(APIView, PageNumberPagination):
    def get(self, request: Request) -> Response:
        pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, request, view=self)
        serializer = PetSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        group_data = serializer.validated_data.pop("group")

        traits_data = serializer.validated_data.pop("traits")

        new_pet = Pet(**serializer.validated_data)

        try:
            group = Group.objects.get(
                scientific_name__icontains=group_data["scientific_name"]
            )
        except Group.DoesNotExist:
            group = Group.objects.create(**group_data)

        new_pet.group = group

        new_pet.save()

        for trait in traits_data:
            try:
                find_trait = Trait.objects.get(name__iendswith=trait["name"])
            except:
                find_trait = Trait.objects.create(**trait)

            new_pet.traits.add(find_trait)

        serializer = PetSerializer(new_pet)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
