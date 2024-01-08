import json
import pika

from contacts import Contact


def send_message(ch, method, properties, body):
    message = json.loads(body.decode())
    print(f" [x] Received {message}")
    Contact.objects(id=message['id']).update(sent=True)
    print(f" [x] Sent: {method.delivery_tag}")


if __name__ == '__main__':
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost',
            port=5672,
            credentials=credentials
        )
    )
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue='send_via_sms',
        on_message_callback=send_message,
        auto_ack=True
    )
    channel.basic_consume(
        queue='send_via_email',
        on_message_callback=send_message,
        auto_ack=True
    )
    print(' [*] Waiting for messages. To exit press CTRL+C')
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print('CTRL+C pressed')
