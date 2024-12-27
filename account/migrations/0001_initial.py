from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('nickname', models.CharField(max_length=50, unique=True)),
                ('profile_picture', models.URLField(null=True)),
                ('kakao_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
