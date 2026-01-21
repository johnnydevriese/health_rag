from google import genai
from app.core.config import settings

def list_models():
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    print("Available models:")
    for model in client.models.list():
        print(f"- {model.name}")

if __name__ == "__main__":
    list_models()
