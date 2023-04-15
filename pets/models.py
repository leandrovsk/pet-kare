from django.db import models


class Gender(models.TextChoices):
    MALE = "male"
    FEMALE = "female"
    DEFAULT = "not informed"


class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(
        max_length=20,
        choices=Gender.choices,
        default=Gender.DEFAULT,
    )

    group = models.ForeignKey(
        "groups.Group", on_delete=models.PROTECT, related_name="pets"
    )

    def __repr__(self) -> str:
        return f"<Pet ({self.id}) - {self.name}>"
