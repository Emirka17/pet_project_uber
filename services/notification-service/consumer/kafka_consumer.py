from kafka import KafkaConsumer
import json
import threading
import logging
from services.sender import NotificationSender
from models.notification import NotificationEvent, PushNotification
from config import KAFKA_BOOTSTRAP_SERVERS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NotificationConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'notifications.send',
            bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            group_id='notification-service-group',
            auto_offset_reset='earliest'
        )

    def start_consuming(self):
        logger.info("Starting notification consumer...")
        for message in self.consumer:
            try:
                event_data = message.value
                logger.info(f"Received notification event: {event_data}")
                
                # Process different types of notifications
                if event_data.get('event_type') == 'ride_assigned':
                    self._handle_ride_assigned(event_data)
                elif event_data.get('event_type') == 'ride_completed':
                    self._handle_ride_completed(event_data)
                elif event_data.get('event_type') == 'payment_processed':
                    self._handle_payment_processed(event_data)
                else:
                    self._handle_generic_notification(event_data)
                    
            except Exception as e:
                logger.error(f"Error processing notification: {e}")

    def _handle_ride_assigned(self, event_data):
        notification = PushNotification(
            user_id=event_data['user_id'],
            title="Водитель найден!",
            message=f"Ваш водитель уже в пути. Машина: {event_data.get('metadata', {}).get('car_model', 'Неизвестно')}",
            data={"ride_id": event_data.get('metadata', {}).get('ride_id')}
        )
        NotificationSender.send_push_notification(notification)

    def _handle_ride_completed(self, event_data):
        notification = PushNotification(
            user_id=event_data['user_id'],
            title="Поездка завершена",
            message=f"Спасибо за поездку! Стоимость: ${event_data.get('metadata', {}).get('amount', 0)}",
            data={"ride_id": event_data.get('metadata', {}).get('ride_id')}
        )
        NotificationSender.send_push_notification(notification)

    def _handle_payment_processed(self, event_data):
        if event_data.get('metadata', {}).get('status') == 'succeeded':
            notification = PushNotification(
                user_id=event_data['user_id'],
                title="Оплата прошла успешно",
                message=f"Оплата поездки на сумму ${event_data.get('metadata', {}).get('amount', 0)} прошла успешно",
                data={"payment_id": event_data.get('metadata', {}).get('payment_id')}
            )
        else:
            notification = PushNotification(
                user_id=event_data['user_id'],
                title="Проблема с оплатой",
                message="Не удалось обработать платеж. Пожалуйста, проверьте данные карты.",
                data={"payment_id": event_data.get('metadata', {}).get('payment_id')}
            )
        NotificationSender.send_push_notification(notification)

    def _handle_generic_notification(self, event_data):
        notification = PushNotification(
            user_id=event_data['user_id'],
            title=event_data.get('title', 'Уведомление'),
            message=event_data.get('message', ''),
            data=event_data.get('metadata')
        )
        NotificationSender.send_push_notification(notification)

def start_consumer():
    consumer = NotificationConsumer()
    consumer_thread = threading.Thread(target=consumer.start_consuming)
    consumer_thread.daemon = True
    consumer_thread.start()
    return consumer_thread
