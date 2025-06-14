from fastapi import FastAPI, Request
from app.config import settings

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API de WhatsApp + OpenAI + Google Sheets corriendo!"}

# Endpoint de prueba para Twilio webhook (se completará luego)
@app.post("/webhook/twilio")
async def twilio_webhook(request: Request):
    form = await request.form()
    return {"status": "ok", "data": dict(form)} 