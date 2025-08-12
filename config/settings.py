import os

BASE_URL = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")
TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))
