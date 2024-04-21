from starlette.config import Config
from datetime import timedelta

# Initialize Config object with path to .env file
try:
    config = Config(".env")
except FileNotFoundError as e:
    print(e)

# Get database URLs from the config object
db_url = config.get("DB_URL")
test_db_url = config.get("TEST_DB_URL")

access_expiry_time = timedelta(minutes=int(config.get("ACCESS_EXPIRY_TIME")))
refresh_expiry_time = timedelta(days=int(config.get("REFRESH_EXPIRY_TIME")))

secret_key = config.get("SECRET_KEY")
algorithm = config.get("ALGORITHM")

admin_name = config.get('ADMIN_EMAIL')
admin_password = config.get('ADMIN_PASSWORD')