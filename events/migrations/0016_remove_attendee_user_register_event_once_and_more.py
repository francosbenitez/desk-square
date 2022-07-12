# Generated by Django 4.0.5 on 2022-07-02 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0015_attendee_email_attendee_guest_attendee_name_and_more"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="attendee",
            name="user_register_event_once",
        ),
        migrations.AddConstraint(
            model_name="attendee",
            constraint=models.UniqueConstraint(
                fields=("email", "event"), name="email_register_event_once"
            ),
        ),
    ]
