from django.shortcuts import render

from rest_framework.views import APIView, Request, Response, status

from rest_framework.pagination import PageNumberPagination

from .models import Pet

from groups.models import Group

from traits.models import Trait

from .serializers import PetSerializer

from django.shortcuts import get_object_or_404


class PetView(APIView, PageNumberPagination):
    def get(self, request: Request) -> Response:
        trait = request.query_params.get("trait", None)

        pets = Pet.objects.all()

        if trait:
            pets = Pet.objects.filter(traits__name=trait)

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


class PetDetailView(APIView):
    def get(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        group_data: dict = serializer.validated_data.pop("group", None)

        if group_data:
            try:
                group = Group.objects.get(
                    scientific_name__icontains=group_data["scientific_name"]
                )
            except Group.DoesNotExist:
                group = Group.objects.create(**group_data)

            pet.group = group

        traits_data: dict = serializer.validated_data.pop("traits", None)

        if traits_data:
            pet.traits.set({})
            for trait in traits_data:
                try:
                    find_trait = Trait.objects.get(name__iendswith=trait["name"])
                except:
                    find_trait = Trait.objects.create(**trait)

            pet.traits.add(find_trait)

        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)

        pet.save()
        serializer = PetSerializer(pet)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        pet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
