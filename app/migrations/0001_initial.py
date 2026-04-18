from tortoise import migrations
from tortoise.migrations import operations as ops
from tortoise.fields.base import OnDelete
from uuid import uuid4
from tortoise import fields

class Migration(migrations.Migration):
    initial = True

    operations = [
        ops.CreateModel(
            name='Event',
            fields=[
                ('id', fields.UUIDField(primary_key=True, default=uuid4, unique=True, db_index=True)),
                ('name', fields.CharField(max_length=100)),
                ('created_at', fields.DatetimeField(auto_now=False, auto_now_add=True)),
                ('finished_at', fields.DatetimeField(null=True, auto_now=False, auto_now_add=False)),
            ],
            options={'table': 'event', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
        ops.CreateModel(
            name='State',
            fields=[
                ('id', fields.IntField(generated=True, primary_key=True, unique=True, db_index=True)),
                ('event', fields.OneToOneField('models.Event', source_field='event_id', null=True, db_constraint=True, to_field='id', on_delete=OnDelete.RESTRICT)),
                ('singleton', fields.IntField(default=1, unique=True)),
                ('start_date', fields.DatetimeField(null=True, auto_now=False, auto_now_add=False)),
            ],
            options={'table': 'state', 'app': 'models', 'pk_attr': 'id'},
            bases=['Model'],
        ),
    ]
