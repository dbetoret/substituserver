# Generated by Django 4.1.3 on 2022-11-30 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('absencies', '0002_rename_id_horari_absencia_horari_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absencia',
            name='data_fi',
            field=models.DateField(null=True, verbose_name="Data d'acabament"),
        ),
        migrations.AlterField(
            model_name='absencia',
            name='hora_fi',
            field=models.TimeField(null=True, verbose_name="Hora d'acabament"),
        ),
        migrations.AlterField(
            model_name='absencia',
            name='hora_ini',
            field=models.TimeField(null=True, verbose_name="Hora d'inici"),
        ),
        migrations.AlterField(
            model_name='guardia',
            name='substitut',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='absencies.usuari'),
        ),
        migrations.AlterField(
            model_name='horari',
            name='espai',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='absencies.espai'),
        ),
        migrations.AlterField(
            model_name='horari',
            name='grup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='absencies.grup'),
        ),
        migrations.AlterField(
            model_name='horari',
            name='materia',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='absencies.materia'),
        ),
    ]
