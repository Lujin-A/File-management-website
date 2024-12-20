# Generated by Django 4.0.3 on 2024-11-02 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_album_albummediafiles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='display_pattern',
            field=models.CharField(choices=[('carousel', 'Carousel'), ('grid', 'Grid View'), ('slideshow', 'Slideshow')], max_length=20),
        ),
        migrations.AlterField(
            model_name='uploadedfile',
            name='file_location',
            field=models.FileField(upload_to='core/uploads/'),
        ),
    ]
