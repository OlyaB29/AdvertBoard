# Generated by Django 4.1.1 on 2022-10-10 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0002_advertcharvalue_value_alter_advert_title_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='place',
            options={'ordering': ('region', 'city'), 'verbose_name': 'Город/район', 'verbose_name_plural': 'Города/районы'},
        ),
        migrations.AlterModelOptions(
            name='region',
            options={'ordering': ('id',), 'verbose_name': 'Область', 'verbose_name_plural': 'Области/г.Минск'},
        ),
        migrations.AlterModelOptions(
            name='value',
            options={'verbose_name': 'Значение', 'verbose_name_plural': 'Значения характеристик'},
        ),
        migrations.AddField(
            model_name='category',
            name='full_name',
            field=models.CharField(default='full', max_length=100, unique=True, verbose_name='Полное название'),
        ),
        migrations.AddField(
            model_name='characteristic',
            name='full_name',
            field=models.CharField(default='full', max_length=100, unique=True, verbose_name='Полное наименование'),
        ),
        migrations.AlterField(
            model_name='advert',
            name='date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата создания или обновления'),
        ),
        migrations.AlterField(
            model_name='advert',
            name='is_new',
            field=models.CharField(choices=[('1', 'Новое'), ('2', 'Б/у')], max_length=5, verbose_name='Состояние'),
        ),
        migrations.RemoveField(
            model_name='advertcharvalue',
            name='advert',
        ),
        migrations.AlterField(
            model_name='category',
            name='characteristics',
            field=models.ManyToManyField(blank=True, related_name='categories', to='advertisements.characteristic', verbose_name='Характеристики'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='characteristic',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата создания или обновления'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='advertisements/', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Имя'),
        ),
        migrations.AddField(
            model_name='advertcharvalue',
            name='advert',
            field=models.ManyToManyField(blank=True, to='advertisements.advert', verbose_name='Объявление'),
        ),
    ]
