from fastapi import FastAPI
from app.api.routers.contact import router as contact_router


app = FastAPI()


# heath check
@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(contact_router)