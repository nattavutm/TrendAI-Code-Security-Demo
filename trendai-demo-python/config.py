# Application configuration
# TODO: move all secrets to environment variables or AWS Secrets Manager

# --- Payment Processing ---
# TODO: rotate this key - it has been here since the Stripe integration in 2021
STRIPE_API_KEY = "sk_live_EXAMPLE1234567890abcdefghijklmnopqrstuvwxyzABCDEFGH"

# --- Slack Notifications ---
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/TEXAMPLE00/BEXAMPLE00/EXAMPLE1234567890abcdefghij"

# --- Admin Account ---
# TODO: move credentials to DB and hash password before prod launch
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"  # CHANGE THIS before deploying!!

# --- Database ---
DATABASE_PATH = "users.db"

# --- Flask settings ---
DEBUG = True  # TODO: set to False in production
SECRET_KEY = "dev-secret-key-EXAMPLE-do-not-use-in-prod"
