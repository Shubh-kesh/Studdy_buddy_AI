import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        self.MODEL_NAME = "llama-3.1-8b-instant"
        self.TEMPERATURE = 0.9 # Controls the randomness of the model's outpu

        self.MAX_RETRY = 3 # Maximum number of retries for API calls in case of network issues



settings = Settings()