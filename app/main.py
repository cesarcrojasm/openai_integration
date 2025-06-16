import os
from fastapi import FastAPI, Request
from app.config import settings
import requests
from app.services.drive_service import upload_file_to_drive
from app.services.sheets_service import append_row_to_sheet
from datetime import datetime
import pytz
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API de WhatsApp + OpenAI + Google Sheets corriendo!"}

# Endpoint de prueba para Twilio webhook (se completará luego)
@app.post("/webhook/twilio")
async def twilio_webhook(request: Request):
    form = await request.form()
    from_number = form.get("From")
    message_body = form.get("Body")
    num_media = int(form.get("NumMedia", 0))

    print(f"Mensaje recibido de {from_number}: {message_body}")

    if num_media > 0:
        media_url = form.get("MediaUrl0")
        media_type = form.get("MediaContentType0")
        print(f"Imagen recibida: {media_url} (tipo: {media_type})")

        # Crea la carpeta 'images' si no existe
        os.makedirs("images", exist_ok=True)
        extension = media_type.split("/")[-1]
        filename = f"images/imagen_{from_number.replace(':', '_')}.{extension}"

        # Descarga y guarda la imagen
        response = requests.get(media_url)
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Imagen guardada como {filename}")

        file_id, webViewLink = upload_file_to_drive(filename, os.path.basename(filename), folder_id="1ba3-RuKdhKBXnHeOfDcPyeqmPZzhEVOA")
        print(f"Enlace de la imagen en Google Drive: {webViewLink}")

        # Obtén el timestamp en horario America/Bogota
        tz = pytz.timezone('America/Bogota')
        timestamp = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

        # ID de tu Google Sheet
        #spreadsheet_id = settings.GOOGLE_SHEETS_ID
        spreadsheet_id = "1Xfo9yXEuMvtIMgdlsiNzp5UhQWry9GFWtImmAMKBKOk"
        print(f"Spreadsheet ID: {spreadsheet_id}")
        # Datos a guardar (si no hay imagen, webViewLink será "")
        values = [from_number, webViewLink, timestamp, message_body]

        # Guarda en Google Sheets
        append_row_to_sheet(spreadsheet_id, values)
        print("Datos guardados en Google Sheets")      
        return "OK" 