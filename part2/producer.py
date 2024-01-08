import json
from random import randint
from faker import Faker
import pika

from contacts import Contact

NUMBER_OF_CONTACTS = 20


def generate_fake_contacts(n_contacts: int = NUMBER_OF_CONTACTS):
    fake_data = Faker()
    for _ in range(n_contacts):
        Contact(
            fullname=fake_data.name(),
            email=fake_data.email(),
            phone=fake_data.phone_number(),
            send_via_sms=bool(randint(0, 1))
        ).save()


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=credentials
        )
    )
    channel = connection.channel()
    channel.exchange_declare(exchange='messaging', exchange_type='direct')
    channel.queue_declare(queue='send_via_sms', durable=True)
    channel.queue_bind(exchange='messaging', queue='send_via_sms')
    channel.queue_declare(queue='send_via_email', durable=True)
    channel.queue_bind(exchange='messaging', queue='send_via_email')

    for contact in Contact.objects(sent=False):
        message = {
            "id": str(contact.id),
            "fullname": contact.fullname
        }
        queue = "send_via_sms" if contact.send_via_sms else "send_via_email"
        channel.basic_publish(
            exchange="messaging",
            routing_key=queue,
            body=json.dumps(message).encode(encoding="UTF-8"),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
        print(f" [x] {queue} {message}")

    connection.close()


if __name__ == '__main__':
    generate_fake_contacts()
    main()
