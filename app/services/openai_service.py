import openai
import base64
from app.config import settings

openai.api_key = settings.OPENAI_API_KEY

def extract_number_from_image(image_path):
    print(f"image_path: {image_path}")
    with open(image_path, "rb") as image_file:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extrae el número que aparece en la imagen. Solo responde el número, sin texto adicional."},
                        {
                            "type": "image_url", 
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64.b64encode(image_file.read()).decode()}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=10
        )
        print(f"response: {response}")
    print(response.choices[0])
    # Extrae solo el número de la respuesta
    return response.choices[0].message.content.strip()