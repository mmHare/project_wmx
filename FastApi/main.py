import datetime
import json
from pathlib import Path
from contextlib import asynccontextmanager
import time
from typing import Optional

from fastapi import FastAPI
from tinydb import Query, TinyDB
import asyncpg

# ------------------------------
# Load configuration
# ------------------------------
CONFIG_PATH = Path("FastApi/config.json")


def load_config(path: Path):
    with path.open() as f:
        return json.load(f)


config = load_config(CONFIG_PATH)

# ------------------------------
# Lifespan context
# ------------------------------
postgres_pool: asyncpg.pool.Pool | None = None
api_db: TinyDB | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global postgres_pool, api_db

    # Startup
    api_db = TinyDB(config["api_db"]["path"])
    postgres_pool = await asyncpg.create_pool(
        user=config["postgres"]["user"],
        password=config["postgres"]["password"],
        database=config["postgres"]["database"],
        host=config["postgres"]["host"],
        port=config["postgres"].get("port", 5432),
        min_size=1,
        max_size=5,
    )
    print("Initialized TinyDB and PostgreSQL pool")
    yield   # 🚀 App runs while control is here

    # Shutdown
    if postgres_pool:
        await postgres_pool.close()
    if api_db:
        api_db.close()
    print("Closed TinyDB and PostgreSQL pool")

# ------------------------------
# FastAPI app
# ------------------------------
app = FastAPI(lifespan=lifespan, title="My FastAPI Unit")

# ------------------------------
# Example route
# ------------------------------


@app.get("/health")
async def health_check():
    async with postgres_pool.acquire() as conn:
        result = await conn.fetchval("SELECT 1")
    return {
        "status": "ok",
        "api_db_tables": list(api_db.tables()),
        "postgres_test": result,
    }


@app.get("/get-conv")
def get_conversation(user_guid: str, recipient_guid: str, rec_limit: Optional[int] = 10, not_received: Optional[bool] = False):
    conversation_list = []

    User = Query()
    user = api_db.get(User.guid == user_guid)
    if user:
        for message in user["messages"][recipient_guid]:
            conversation_list.append(
                (user_guid, message["text"], message["date_post"], message["received"]))

    Recipient = Query()
    recipient = api_db.get(Recipient.guid == recipient_guid)
    if recipient:
        for message in recipient["text"][user_guid]:
            if not_received and message["received"]:
                continue
            conversation_list.append(
                (recipient_guid, message["text"], message["date_post"], message["received"]))

    conversation_list.sort(key=lambda m: m[2])

    if rec_limit:
        conversation_list = conversation_list[-rec_limit:]

    return [f"{sender}: {text}" for sender, text, _, _ in conversation_list]


@app.post("/send-msg")
async def send_message(user_guid: str, recipient_guid: str, message_text: str):
    sql_text = "SELECT login FROM users WHERE (deleted_at is null) and (guid = $1)"
    result = await postgres_pool.fetchrow(sql_text, user_guid)
    if not result:
        return "User does not exist"
    login = result[0]

    sql_text = "SELECT login FROM users WHERE (deleted_at is null) and (guid = $1)"
    result = await postgres_pool.fetchrow(sql_text, recipient_guid)
    if not result:
        return "Recipient does not exist"

    User = Query()
    user = api_db.get(User.guid == user_guid)
    if not user:
        user = {"guid": user_guid, "nickname": login, "messages": {}}

    user["messages"].setdefault(recipient_guid, []).append({
        "text": message_text,
        "date_post": datetime.datetime.now().isoformat(),
        "received": False
    })
    api_db.upsert(user, User.guid == user_guid)
    return "Succes"


# ------------------------------
# Run with uvicorn
# ------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
