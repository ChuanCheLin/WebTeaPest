# Generated by Django 3.0.3 on 2022-08-04 04:15

import datetime
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields
import tealinebot.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('TeaData', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detection',
            fields=[
                ('pred_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('img_name', models.CharField(max_length=100, null=True)),
                ('box_id', models.CharField(help_text='ABCDE', max_length=1)),
                ('pred_cls', models.CharField(max_length=20)),
                ('html_file', models.CharField(max_length=20, null=True)),
                ('score', models.FloatField()),
                ('xmin', models.IntegerField()),
                ('ymin', models.IntegerField()),
                ('xmax', models.IntegerField()),
                ('ymax', models.IntegerField()),
                ('context', models.TextField(help_text='A: 赤葉枯病 score: 0.995', max_length=100)),
            ],
            options={
                'ordering': ['img_data', 'box_id'],
            },
        ),
        migrations.CreateModel(
            name='LineImg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_id', models.CharField(default='unknow', help_text='image name of the prediction', max_length=100)),
                ('img_url', models.ImageField(upload_to=tealinebot.models.custum_path)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('pred_num', models.IntegerField(default=0)),
                ('altitude', models.CharField(blank=True, help_text='海拔高度', max_length=20)),
                ('gps', models.CharField(blank=True, help_text='gps 位址', max_length=30)),
                ('city', smart_selects.db_fields.GroupedForeignKey(group_field='County', null=True, on_delete=django.db.models.deletion.SET_NULL, to='TeaData.City')),
                ('county', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='TeaData.County')),
            ],
            options={
                'ordering': ['-date'],
                'get_latest_by': 'date',
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedbackID', models.CharField(default='2011270122A', max_length=20)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('issue', models.CharField(choices=[('wrong', '病蟲害種類誤判'), ('background', '背景或健康葉片被誤判'), ('nodetect', '病蟲害未被辨識'), ('other', '其他')], default='other', max_length=50)),
                ('feedback', models.TextField(blank=True, help_text='user feedback', max_length=100, null=True)),
                ('true_label', models.CharField(choices=[('mosquito_early', 'tea mosquito-early'), ('mosquito_late', 'tea mosquito-late'), ('brownblight', 'brown blight'), ('fungi_early', 'fungi disease-early'), ('blister', 'blister blight'), ('algal', 'algal leaf spot'), ('miner', 'leaf miner'), ('thrips', 'tea thrips'), ('orient', 'oriental tea tortrix'), ('moth', 'small tea tortrix-bite'), ('tortrix', 'small tea tortrix-roll'), ('flushworm', 'tea flushworm'), ('not', 'not a disease'), ('unknown', 'unknown disease')], max_length=20, null=True)),
                ('review', models.TextField(blank=True, help_text='profesional review', max_length=100, null=True)),
                ('contact', models.EmailField(blank=True, max_length=254, null=True)),
                ('finishCheck', models.BooleanField(default=False)),
                ('pred', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tealinebot.Detection')),
            ],
            options={
                'ordering': ['-date'],
                'get_latest_by': 'date',
            },
        ),
        migrations.AddField(
            model_name='detection',
            name='img_data',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tealinebot.LineImg'),
        ),
    ]
