# Generated by Django 2.2 on 2022-08-04 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0004_book_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='Rating',
        ),
    ]
