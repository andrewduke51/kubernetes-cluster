# shared.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redislite

# Create a Limiter instance here
limiter = Limiter(key_func=get_remote_address)
redis_server = redislite.StrictRedis()
