from mongoengine import Document, connect
from mongoengine.fields import StringField, BooleanField

connect(host="mongodb://localhost:27017/my_db")


class Contact(Document):
    fullname = StringField()
    email = StringField()
    phone = StringField()
    sent = BooleanField(default=False)
    send_via_sms = BooleanField(default=False)
