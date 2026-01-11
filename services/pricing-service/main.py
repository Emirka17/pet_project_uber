from fastapi import FastAPI
from routers import pricing
import uvicorn

app = FastAPI(title="Pricing Service", version="1.0.0")

# Include routers
app.include_router(pricing.router)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8006)
