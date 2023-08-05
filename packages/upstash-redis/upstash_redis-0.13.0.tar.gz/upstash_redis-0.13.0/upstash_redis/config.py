"""
For now, we'll store the defaults here.
In the future, we might have an option to load from .env in development environments.
"""

REST_ENCODING = "base64"

REST_RETRIES: int = 1

REST_RETRY_INTERVAL: int = 3  # Seconds.

FORMAT_RETURN: bool = True

ALLOW_TELEMETRY: bool = True
