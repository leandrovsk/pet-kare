# Generated by Django 4.2 on 2023-04-15 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("groups", "0001_initial"),
        ("pets", "0002_rename_weigth_pet_weight"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pet",
            name="group",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="pets",
                to="groups.group",
            ),
            preserve_default=False,
        ),
    ]