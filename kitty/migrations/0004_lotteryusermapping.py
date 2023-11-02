# Generated by Django 4.2.6 on 2023-10-23 06:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kitty', '0003_alter_lottery_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='LotteryUserMapping',
            fields=[
                ('isActive', models.BooleanField(default=True)),
                ('groupId', models.CharField(default=1, max_length=40)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
                ('updatedDate', models.DateTimeField(auto_now=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('lotteryNumber', models.IntegerField()),
                ('userName', models.CharField(max_length=50)),
                ('additionalAmount', models.FloatField(blank=True, null=True)),
                ('discount', models.FloatField()),
                ('createdBy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL)),
                ('lotteryId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='kitty.lottery')),
                ('updatedBy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL)),
                ('userId', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='kitty.user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]