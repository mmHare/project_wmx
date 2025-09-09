import datetime
import json
from pathlib import Path
from contextlib import asynccontextmanager
import socket
import time
from typing import Optional

from fastapi import FastAPI
from tinydb import Query, TinyDB
import asyncpg

# ------------------------------
# Load configuration
# ------------------------------
CONFIG_PATH = Path("./config.json")


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

    # register API address in database
    sql_text = "INSERT INTO configuration (key_name, value_str, value_int) VALUES ($1, $2, $3) ON CONFLICT (key_name) DO UPDATE SET value_str = $2, value_int = $3;"
    # hostname = socket.gethostname()
    # ip_addr = socket.gethostbyname(hostname)
    ip_addr = "192.168.0.30"
    api_socket = 8000
    await postgres_pool.execute(sql_text, "api_address", ip_addr, api_socket)

    print("Initialized TinyDB and PostgreSQL pool")
    yield   # App runs while control is here

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


@app.get("/get-msg-count")
def get_msg_count(user_guid: str, peer_guid: str, new_msg: Optional[bool] = True):
    result = 0
    Peer = Query()
    peer = api_db.get(Peer.guid == peer_guid)
    if peer:
        result = len([m for m in peer["messages"][user_guid]
                     if (not new_msg) or (not m["received"])])
    return {"msg-count": result}


@app.get("/get-conv")
def get_conversation(user_guid: str, peer_guid: str, rec_limit: Optional[int] = 10, not_received: Optional[bool] = False):
    conversation_list = []

    User = Query()
    user = api_db.get(User.guid == user_guid)
    if user:
        for message in user["messages"][peer_guid]:
            conversation_list.append(
                {"nickname": user["nickname"], "text": message["text"], "date_post": message["date_post"], "received": message["received"]})

    Peer = Query()
    peer = api_db.get(Peer.guid == peer_guid)
    if peer:
        for message in peer["messages"][user_guid]:
            if not_received and message["received"]:
                continue
            conversation_list.append(
                {"nickname": peer["nickname"], "text": message["text"], "date_post": message["date_post"], "received": message["received"]})
            message["received"] = True

    api_db.update(peer, Peer.guid == peer_guid)

    conversation_list.sort(key=lambda m: m["date_post"])

    if rec_limit:
        conversation_list = conversation_list[-rec_limit:]

    return conversation_list

    # return [f"{sender}: {text}" for sender, text, _, _ in conversation_list]


@app.post("/send-msg")
async def send_message(user_guid: str, peer_guid: str, message_text: str):
    sql_text = "SELECT login FROM users WHERE (deleted_at is null) and (guid = $1)"
    result = await postgres_pool.fetchrow(sql_text, user_guid)
    if not result:
        return "User does not exist"
    login = result[0]

    sql_text = "SELECT login FROM users WHERE (deleted_at is null) and (guid = $1)"
    result = await postgres_pool.fetchrow(sql_text, peer_guid)
    if not result:
        return "Recipient does not exist"

    User = Query()
    user = api_db.get(User.guid == user_guid)
    if not user:
        user = {"guid": user_guid, "nickname": login, "messages": {}}

    user["messages"].setdefault(peer_guid, []).append({
        "text": message_text,
        "date_post": datetime.datetime.now().isoformat(),
        "received": False
    })
    api_db.upsert(user, User.guid == user_guid)
    return message_text


# ------------------------------
# Run with uvicorn
# ------------------------------
if __name__ == "__main__":
    import uvicorn
    # hostname = socket.gethostname()
    # ip_addr = socket.gethostbyname(hostname)
    ip_addr = "0.0.0.0"
    api_socket = 8000
    uvicorn.run("main:app", host=ip_addr, port=api_socket, reload=True)
