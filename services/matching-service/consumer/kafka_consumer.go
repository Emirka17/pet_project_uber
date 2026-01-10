// services/matching-service/consumer/kafka_consumer.go
package consumer

import (
	"context"
	"log"

	"github.com/segmentio/kafka-go"
)

type KafkaConsumer struct {
	Reader *kafka.Reader
}

func NewKafkaConsumer(brokers, groupID, topic string) *KafkaConsumer {
	reader := kafka.NewReader(kafka.ReaderConfig{
		Brokers:  []string{brokers},
		GroupID:  groupID,
		Topic:    topic,
		MinBytes: 10e3, // 10KB
		MaxBytes: 10e6, // 10MB
	})

	return &KafkaConsumer{Reader: reader}
}

func (c *KafkaConsumer) Consume(ctx context.Context, handler func([]byte) error) {
	for {
		msg, err := c.Reader.ReadMessage(ctx)
		if err != nil {
			log.Printf("Ошибка чтения сообщения: %v", err)
			continue
		}

		log.Printf("Получено сообщение: topic=%s partition=%d offset=%d", msg.Topic, msg.Partition, msg.Offset)

		if err := handler(msg.Value); err != nil {
			log.Printf("Ошибка обработки сообщения: %v", err)
			// Не подтверждаем, чтобы Kafka перепослала
			continue
		}

		// Подтверждаем обработку
		if err := c.Reader.CommitMessages(ctx, msg); err != nil {
			log.Printf("Ошибка подтверждения: %v", err)
		}
	}
}

func (c *KafkaConsumer) Close() error {
	return c.Reader.Close()
}
