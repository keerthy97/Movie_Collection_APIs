# Generated by Django 4.2.7 on 2023-11-16 15:08

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Collection",
            fields=[
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField()),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Movie",
            fields=[
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("genres", models.CharField(max_length=250)),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MovieCollection",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "collection",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="collections_app.collection",
                    ),
                ),
                (
                    "movie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="collections_app.movie",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="collection",
            name="movies",
            field=models.ManyToManyField(
                related_name="collections",
                through="collections_app.MovieCollection",
                to="collections_app.movie",
            ),
        ),
    ]
