from fastapi import FastAPI
from routers import notifications
from consumers.kafka_consumer import start_consumer
import uvicorn

app = FastAPI(title="Notification Service", version="1.0.0")

# Include routers
app.include_router(notifications.router)

# Start Kafka consumer
consumer_thread = start_consumer()

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8008)
