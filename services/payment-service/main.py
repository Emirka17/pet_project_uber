from fastapi import FastAPI
from routers import payments
import uvicorn

app = FastAPI(title="Payment Service", version="1.0.0")

# Include routers
app.include_router(payments.router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8007)
