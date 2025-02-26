import pika

def send_push():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='pingpong')  
    channel.queue_declare(queue='pingpong_control') 

    # Check if the control queue is empty
    method_frame, _, _ = channel.basic_get(queue='pingpong_control')

    if method_frame:
        print("Sorry, PingPong is already in action.")
    else:

        # We push for the first time and make the 
        channel.basic_publish(exchange='',
                              routing_key='pingpong_control',
                              body='active')
        
        # Start the Ping-Pong 
        channel.basic_publish(exchange='',
                              routing_key='pingpong',
                              body='Push')
        print("Sent 'Push' to start PingPong")

    connection.close()

if __name__ == "__main__":
    send_push()
