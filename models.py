from os import getenv

from dotenv import load_dotenv
from peewee import *
from playhouse.postgres_ext import *

load_dotenv()

# connect to postgres
pg_db = PostgresqlDatabase(
    getenv('POSTGRES_DATABASE'),
    user=getenv('POSTGRES_USERNAME'),
    password=getenv('POSTGRES_PASSWORD'),
    host=getenv('POSTGRES_HOST'),
    port=getenv('POSTGRES_PORT')
)

# create models


class Article(Model):
    title = CharField(max_length=500, index=True)
    text = TextField()
    link = CharField(max_length=500)

    class Meta:
        database = pg_db
        table_name = 'articles'


class Paraphrase(Model):
    pair = ArrayField(CharField)
    score = FloatField()

    class Meta:
        database = pg_db
        table_name = 'paraphrases'


# create tables
if __name__ == '__main__':
    pg_db.connect()
    pg_db.drop_tables([Article, Paraphrase])
    pg_db.create_tables([Article, Paraphrase])
