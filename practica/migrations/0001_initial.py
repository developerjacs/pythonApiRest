# Generated by Django 3.0.5 on 2020-11-12 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='', max_length=70)),
                ('apellido1', models.CharField(default='', max_length=70)),
                ('apellido2', models.CharField(default='', max_length=70)),
                ('nombre_usuario', models.CharField(default='', max_length=70)),
                ('fecha_nacimiento', models.DateField(blank=True)),
                ('fecha_registro', models.DateField(blank=True)),
                ('biografia', models.CharField(blank=True, max_length=150)),
                ('seguidos', models.ManyToManyField(to='practica.Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='', max_length=70)),
                ('descripcion', models.CharField(default='', max_length=200)),
                ('graffiti', models.CharField(default='', max_length=70)),
                ('fecha', models.DateTimeField()),
                ('autor', models.CharField(default='', max_length=70)),
                ('ubicacion', models.CharField(default='', max_length=70)),
                ('likes', models.ManyToManyField(blank=True, related_name='Likes', to='practica.Usuario')),
                ('publicador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='practica.Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensaje', models.CharField(default='', max_length=70)),
                ('fecha', models.DateTimeField()),
                ('publicacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='practica.Publicacion')),
                ('publicador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='practica.Usuario')),
            ],
        ),
    ]
