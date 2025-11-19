import pika
import json
import sys
import os

def main():
    # 1. Credenciales (Las mismas que en Docker y svc-orders)
    credentials = pika.PlainCredentials('admin', 'password')
    
    # 2. Conexión bloqueante (Este script es un proceso background, no una API)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials)
    )
    channel = connection.channel()

    # 3. Declarar la misma cola (por seguridad, si no existe la crea)
    channel.queue_declare(queue='pedidos_queue', durable=True)

    # 4. Función que se ejecuta cada vez que llega un mensaje
    def callback(ch, method, properties, body):
        datos = json.loads(body)
        print(f" [🔔] NUEVO EVENTO RECIBIDO:")
        print(f"      - Mesa: {datos.get('mesa_qr_id', 'Desconocida')}")
        print(f"      - Total: ${datos.get('total', 0)}")
        print(f"      - Acción: Simulando envío de notificación a cocina...")
        print(" [✅] Procesado.\n")
        
        # IMPORTANTE: Avisar a RabbitMQ que ya terminamos (ACK)
        # Si no hacemos esto, el mensaje vuelve a la cola si el servicio se cae.
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # 5. Configurar el consumo
    channel.basic_qos(prefetch_count=1) # Procesa 1 a la vez
    channel.basic_consume(queue='pedidos_queue', on_message_callback=callback)

    print(' [*] Servicio de Notificaciones esperando pedidos. Presiona CTRL+C para salir.')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrumpido')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)