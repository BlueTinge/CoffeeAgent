import pika
import json
agent_name = 'Watson'
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters(host='128.113.21.86',
                                       virtual_host='/',
                                       credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()


def connect_to_server():
   
    channel.queue_declare(queue='to-agents')
    channel.queue_declare(queue='output-gate')
   
    #channel.exchange_declare(exchange='amq.topic',
                             #type='direct', durable=True)
   
    channel.queue_bind(exchange='amq.topic',
                       queue='to-agents')
    channel.queue_bind(exchange='amq.topic',
                       queue='output-gate')
    return channel

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
      
    msg = json.loads(body);  
      
    reply = {}
    reply['inReplyTo'] = msg['currentState']
    reply['msg.sender'] = agent_name
    reply['transcript'] = 'Hello, would you like to buy my coffee?'
    reply['room'] = 1001
      
    ch.basic_publish(exchange='amq.topic', routing_key='output-gate', body=json.dumps(reply))
connect_to_server();

    #channel.queue_declare(queue='amq.topic')
channel.basic_consume(
    queue='to-agents', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()