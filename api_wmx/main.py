import datetime
import json
from pathlib import Path
from contextlib import asynccontextmanager
import socket
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


def get_local_ip():
    try:
        # connect to an external address, doesn't have to be reachable
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google DNS
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


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
    sql_text = "INSERT INTO configuration (key_name, value_str, value_int) VALUES ($1, $2, $3) \
                ON CONFLICT (key_name) DO UPDATE SET value_str = $2, value_int = $3;"

    ip_addr = get_local_ip()
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

    # messages from User to Peer
    User = Query()
    user = api_db.get(User.guid == user_guid)
    if user:
        for message in user["messages"].get(peer_guid, []):
            conversation_list.append({
                "nickname": user["nickname"],
                "text": message["text"],
                "date_post": message["date_post"],
                "received": message["received"]
            })

    # messages from Peer to User
    Peer = Query()
    peer = api_db.get(Peer.guid == peer_guid)
    if peer:
        is_update = False
        for message in peer["messages"].get(user_guid, []):
            if not_received and message["received"]:
                continue
            conversation_list.append({
                "nickname": peer["nickname"],
                "text": message["text"],
                "date_post": message["date_post"],
                "received": message["received"]
            })
            if not message["received"]:
                message["received"] = True  # set all messages as received
                is_update = True
        if is_update:  # save to database messages if received flag was changed
            api_db.update(peer, Peer.guid == peer_guid)

    conversation_list.sort(key=lambda m: m["date_post"])  # sort by date

    rec_limit = max(0, min(rec_limit, 100))
    conversation_list = conversation_list[-rec_limit:]  # limit the outcome

    return conversation_list


@app.post("/send-msg")
async def send_message(user_guid: str, peer_guid: str, message_text: str):
    # find user login
    sql_text = "SELECT login FROM users WHERE (deleted_at is null) and (guid = $1)"
    result = await postgres_pool.fetchrow(sql_text, user_guid)
    if not result:
        return "User not found"
    login = result[0]

    # find peer login
    sql_text = "SELECT login FROM users WHERE (deleted_at is null) and (guid = $1)"
    result = await postgres_pool.fetchrow(sql_text, peer_guid)
    if not result:
        return "Recipient not found"

    # find messages in db
    User = Query()
    user = api_db.get(User.guid == user_guid)
    if not user:
        user = {"guid": user_guid, "nickname": login, "messages": {}}

    # add posted message to the list and save in db
    user["messages"].setdefault(peer_guid, []).append({
        "text": message_text,
        "date_post": datetime.datetime.now().isoformat(),
        "received": False
    })
    api_db.upsert(user, User.guid == user_guid)
    return message_text


# ------------------------------
# Run
# ------------------------------
if __name__ == "__main__":
    import uvicorn
    ip_addr = "0.0.0.0"
    api_socket = 8000
    uvicorn.run("main:app", host=ip_addr, port=api_socket, reload=True)
