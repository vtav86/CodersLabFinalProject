# Generated by Django 4.0.6 on 2022-08-07 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("gym_app", "0004_remove_visits_member_visits_member"),
    ]

    operations = [
        migrations.RenameField(
            model_name="visits",
            old_name="member",
            new_name="member_number",
        ),
    ]
