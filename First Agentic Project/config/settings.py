from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path(__file__).resolve().parent / 'keys.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    def __init__(self):
        self.PRICE_API_KEY = os.getenv("PRICE_API_KEY")
        self.NEWS_API_KEY = os.getenv("NEWS_API_KEY")
        self.FINANCE_API_KEY = os.getenv("FINANCE_API_KEY")
        self.FALLBACK_API_KEY = os.getenv("FALLBACK_API_KEY")
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.PRICE_API_URL = os.getenv("PRICE_API_URL")
        self.NEWS_API_URL = os.getenv("NEWS_API_URL")
        self.FINANCIAL_REPORT_URL = os.getenv("FINANCIAL_REPORT_URL")
        self.FALLBACK_API_URL = os.getenv("FALLBACK_API_URL")
