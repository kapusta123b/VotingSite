from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='polls_voted',
            field=models.ManyToManyField(blank=True, to='polls.question'),
        ),
    ]
