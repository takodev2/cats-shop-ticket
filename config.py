import os

TOKEN = os.getenv("DISCORD_TOKEN")
ADMIN_ROLE_ID = [int(rid) for rid in os.getenv("ADMIN_ROLE_IDS", "0").split(",") if rid]
ADMIN_GET_ROLE = int(os.getenv("ADMIN_GET_ROLE", 0))
TICKET_CATEGORY_ID = int(os.getenv("TICKET_CATEGORY_ID", 0))
DONE_CATEGORY_ID = int(os.getenv("DONE_CATEGORY_ID", 0))
