from mongoengine import Document, CASCADE
from mongoengine.fields import ListField, StringField, ReferenceField

import connect


class Author(Document):
    fullname = StringField()
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    tags = ListField()
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    quote = StringField()
    meta = {'allow_inheritance': True}
