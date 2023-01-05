import django.contrib.auth.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                 serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True,
                 verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False,
                 help_text='user has all permissions',
                 verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False,
                 help_text='user can log into this admin site.',
                 verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True,
                 help_text='user should be treated as active',
                 verbose_name='active')),
                ('date_joined', models.DateTimeField(
                    default=django.utils.timezone.now,
                 verbose_name='date joined')),
                ('first_name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100, unique=True)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('User', 'authorized'),
                 ('Admin', 'admin')], max_length=50)),
                ('groups', models.ManyToManyField(blank=True,
                 help_text='A user will get all permissions',
                 related_name='user_set', related_query_name='user',
                 to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(
                    blank=True, help_text='Specific permissions',
                 related_name='user_set', related_query_name='user',
                 to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'unique_together': {('username', 'email')},
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
