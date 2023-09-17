import redislite

# Create an in-memory Redis server using redislite
redis_server = redislite.StrictRedis(
    storage_uri="redis://localhost:6379"
)
