from fastapi import FastAPI
from kafka import KafkaConsumer
import json
import threading
import logging

app = FastAPI(title="Notification Service", version="1.0.0")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Kafka consumer function
def start_kafka_consumer():
    def consume():
        try:
            consumer = KafkaConsumer(
                'notifications.send',
                bootstrap_servers=['kafka:29092'],
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                group_id='notification-service-group',
                auto_offset_reset='earliest'
            )
            
            logger.info("Notification Service: Kafka consumer started")
            for message in consumer:
                try:
                    event_data = message.value
                    logger.info(f"Received notification event: {event_data}")
                    # Здесь будет логика отправки уведомлений
                    logger.info(f"Processing notification for user: {event_data.get('user_id')}")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
        except Exception as e:
            logger.error(f"Kafka consumer error: {e}")
    
    consumer_thread = threading.Thread(target=consume)
    consumer_thread.daemon = True
    consumer_thread.start()
    return consumer_thread

# Start Kafka consumer when app starts
@app.on_event("startup")
async def startup_event():
    start_kafka_consumer()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/")
def root():
    return {"message": "Notification Service is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8008)
