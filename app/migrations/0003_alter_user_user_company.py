# Generated by Django 5.2.4 on 2025-07-10 08:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_name_nodetype_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_company',
            field=models.ForeignKey(db_column='user_company_id', default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='app.usercompany'),
        ),
    ]
