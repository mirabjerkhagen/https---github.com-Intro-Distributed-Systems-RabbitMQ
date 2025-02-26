import pika
import time
import atexit

connection = None
channel = None

# Empty the queue, if the terminal shuts down we clean the cure 

def cleanup():
    """Remove the control message when the server stops."""
    print("\n Cleaning up control queue...")
    if channel and connection:
        channel.queue_purge(queue='pingpong_control')  
        connection.close()
    print("Cleanup complete. Control queue is empty.")

# Starting a Ping Pong Sequnce 

def on_received_message(ch, method, properties, body):
    message = body.decode()
    print(f"Received {message}")

    if message == 'Push':
        print("Starting Ping-Pong sequence.")
        ch.basic_publish(exchange='',
                         routing_key='pingpong',
                         body='Ping')
        print("Sent 'Ping'")

    elif message == 'Ping':
        time.sleep(2)
        ch.basic_publish(exchange='',
                         routing_key='pingpong',
                         body='Pong')
        print("Sent 'Pong'")

    elif message == 'Pong':
        time.sleep(2)
        ch.basic_publish(exchange='',
                         routing_key='pingpong',
                         body='Ping')
        print("Sent 'Ping'")


def start_receiving():
    global connection, channel
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='pingpong')
    channel.queue_declare(queue='pingpong_control')

    # Clear the control queue on startup
    channel.queue_purge(queue='pingpong_control')
    print("Control queue cleared at startup.")

    channel.basic_consume(queue='pingpong',
                          on_message_callback=on_received_message,
                          auto_ack=True)

    print('Waiting for a push. To exit press CTRL+C')
    
    # Register cleanup function on exit
    atexit.register(cleanup)
    
    channel.start_consuming()

if __name__ == "__main__":
    start_receiving()
