import voyageai
from app.core.config import settings
def test_keys():
    print(f"Testing Voyage API Key: {settings.VOYAGE_API_KEY[:5]}...")
    try:
        vc = voyageai.Client(api_key=settings.VOYAGE_API_KEY)
        vc.embed(["test"], model="voyage-3", input_type="document")
        print("Voyage API Key is VALID.")
    except Exception as e:
        print(f"Voyage API Key is INVALID: {e}")

if __name__ == "__main__":
    test_keys()
