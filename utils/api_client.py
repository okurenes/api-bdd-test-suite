import requests
import logging
from config.settings import BASE_URL, TIMEOUT

logger = logging.getLogger(__name__)


class APIClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json", "Accept": "application/json"})

    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET {url}")
        response = self.session.get(url, params=params, timeout=TIMEOUT)
        logger.info(f"Response: {response.status_code}")
        return response

    def post(self, endpoint, payload=None):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST {url} | payload={payload}")
        response = self.session.post(url, json=payload, timeout=TIMEOUT)
        logger.info(f"Response: {response.status_code}")
        return response

    def put(self, endpoint, payload=None):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PUT {url}")
        response = self.session.put(url, json=payload, timeout=TIMEOUT)
        logger.info(f"Response: {response.status_code}")
        return response

    def delete(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        logger.info(f"DELETE {url}")
        response = self.session.delete(url, timeout=TIMEOUT)
        logger.info(f"Response: {response.status_code}")
        return response
