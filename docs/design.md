## Truco!

Progressive web app: (main functrionalities)
--- 
1) Two clients connect via the front-end and once the `server` confirms the conection, the game starts;

2) The `server` will deal cards to each users in the same session, indicate who is hand and witch options are available for the user;

3) The `client` will render with the GUI the cards/options to play (from now on `actions`);

4) Dicotomy of the server:
- If player a is hand, he has the `actions available` and every `action` will generate an event for the server.
- The server needs to process theese information send... and both respond to the `client` a and send information to the `client` b to be updated after every `action` 
5) After every action, swap the `hand-player`


---
Basic Example on how data will move on each row:
---
```json
GameData: {
    "hand":__HAND_ID__,
    "row": __ROW_ID__,
    "isGameOver": false,
    "player0Points": POINTS,
    "player1Points": POINTS,
    ...
}

Player A:{"id": 0, "is_hand": true, "actions": {"cards":..., "options"}}
Player B: {"id": 1, "is_hand": false, "actions": {"cards":..., "options"}}

// Both Players can see their cards but only player A can make decisions

/*Player A takes a move*/
Player A: {"id": 0, "is_hand": false, "actions": {"cards":..., "options"}}
Player B: {"id": 1, "is_hand": true, "actions": {"cards":"[...]", "options":"[...]"}}
```
GameData needs to handle more like a referee type of information.





---

Talking about the game:
At the beginning of the game, two players have to play `n` rows of games until one of them reaches 30 points.
Every row consists of `3` hands, on witch the winner of the hand is the one that better moves does. 2 out of 3 cards-comparassing won but in case of draws the logic will change a little. In hand 1, the envido-betting can be opened an once it is, the game needs to process only this logic.

### Actions example:
```json
// hand 1, 0 moves, player 0 action
{   
    "cards": CARDS,
    options: {
        "envido": [...],
        "truco": [...],
    },
    "in_envido": false,
}
// if player 0 selects an envido option

// hand 1, 1 move, player 1 action:
{   
    "cards": CARDS,
    options: {
        "envido": [...], //Updated
        // "truco": [...],
    },
    "in_envido": true,
}
// Only envido can be played now
```

And in between that communication of both clients, selecting and upgrading the envido-bets, the Desk (or Referee) needs to handle how many points are at risk, and once one of the options is "ACCEPT" or "DONT_ACCEPT"
then the game will give those points to the winner.


```json 
DESK
{
    "points_betted": POINTS,
    "last_bet": BET,
}

```
---




# Abstract Data Types Design


- ## Desk
    - functionalities:
    1) Contain players;
    2) To be a middleware in between players;
    3) To handle game logic;
    - Select round-begginer player;  
    - Deal cards;
    - To Manage betting logic;
    - TODO: ADD MORE `DESK` logic responsabilities
    4) To receive data from the client-side players
    5) To respond AND to send data for players automatically (## Need to investigate how to)
    6) To save important data in a db
    7) (?)

```python
class Desk :
    _deck = TrucoDeck()
    _deck.create_deck()
    _player_0 = Player(0)
    _player_1 = Player(1)
    _bet_values: dict[str, dict[str, int]] = {
        'envido': {
            'envido': 2,
            'real_envido':3,
            # 'falta_envido': 0 Updates dinamically
        },
        'truco':{
            'truco': 2,
            're_truco': 3,
            'vale_cuatro': 4
        }
    }
    _ACCEPT = 'accept'
    _DONT_ACCEPT = 'dont_accept'
    _round: int = -1
    hand: int = 0
    _hand_player: Player
    _foot_player: Player
    _cards_on_the_desk :  dict[int, Card] = {}
    _in_bet: bool

    def innit_game() -> None

    def start_new_row():

```
- Diferenciate when a player has thrown a card or he has started a bet. On endpoint `/player-action` it recieves this structred body: ```json
                    {
                        "id": int,
                        "action": {
                            "card_index": int // -1 (or wont appear) if in bet, else 0 int in between 0 to length of cards list
                            "bet": list[string] // void (or wont appear) if card_index is valid, else bet[0] indicates the type of bet and bet[1] indicates witch bet of the list was wanted.
                        }
                    }
                ``` 
            
`in_bet -> True` 


- ## Player
    1) Contain players options and card
    - Default options must be same for both players on every row... but on each action (only if an option was selected)
    then it they must be updated for both of them depending on the games logic
    - `_is_player_turn` will allow the front-end to know witch instance of a player can send requests to the server (via web-sockets).

    ```python
        _cards: list[Card] = []
        _points: int = 0
        _total_envido: int = 0
        _id: int = id
        _options: PlayerOptions = {}
        _is_player_turn: bool = False
    ```








## WEB SOCKETS EXAMPLE:
```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    await ws.send_json({"event": "welcome"})
```

```js
useEffect(() => {
  const socket = new WebSocket("ws://localhost:8000/ws");

  socket.onmessage = (msg) => {
    const data = JSON.parse(msg.data);
    console.log("Server event:", data);
  };

  return () => socket.close();
}, []);
```





### Most important AI help:
- use of a hub. The methodology of web-socket for online gameing:

- Step 1 — Connection Manager (CORE PIECE)
This object stores all active WebSocket connections and lets you send messages to specific clients or broadcast.
```python
from fastapi import WebSocket
from typing import Dict

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        self.active_connections.pop(client_id, None)

    async def send_to(self, client_id: str, message: str):
        await self.active_connections[client_id].send_text(message)

    async def broadcast(self, message: str):
        for ws in self.active_connections.values():
            await ws.send_text(message)
```

- Step 2 — WebSocket Endpoint

Each client connects with a unique ID:
```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()
manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(client_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()

            # Expect messages like:
            # {"payload": "attack" }

            await handle_message(client_id, data)

    except WebSocketDisconnect:
        manager.disconnect(client_id)
```

- Step 3 — Message Routing Logic
```python
import json

async def handle_message(sender_id: str, raw_data: str):
    data = json.loads(raw_data)

    target_id = data["to"]
    payload = data["payload"]

    # ✅ PROCESS LOGIC (game rules, validation, etc.)
    result = f"Processed '{payload}' from {sender_id}"

    # ✅ SEND RESULT TO TARGET CLIENT
    await manager.send_to(target_id, result)

```
- Explanation of why to use an infinite loop in step-2:
```
The while True means:
🔹 “Keep this connection open and keep listening for messages until the client disconnects.”
A WebSocket is a persistent connection, unlike HTTP which is request → response → done.
So the loop is:
 * Wait for a message
 * Process it
 * Wait for the next one
 * Repeat

Exit when the client disconnects
 * Without the loop, the server would:
 * Accept the connection
 * Read one message
 * Immediately close the socket
→ That would defeat the purpose of WebSockets.
🧠 But wait — doesn’t while True block the server?
Normally yes…
But this is an async function with await.
This line is the key:

 '''data = await websocket.receive_text()'''
That await:
 * Suspends the function
 * Returns control to the event loop
 * Consumes ZERO CPU while waiting
 * Wakes up only when a message arrives

So this is event-driven, not polling.
It behaves conceptually like:
“Call me again only when data arrives.”
So your server is NOT:
 * Spinning
 * Polling
 * Using CPU in a tight loop

It is asleep until a message arrives.
```

- NextJs usage of webSocket:
```js
const ws = new WebSocket("ws://localhost:8000/ws/C2");

ws.onmessage = (event) => {
  console.log("Received:", event.data);
};
```





### User Stories:
 * Lobby:
    - A client enters the web-page and sends a connection request to /enter-lobby
    - The client is asigned to an id (0 or 1) and then it awaits until there are two players in the lobby
    - When there are two players, a message will be brodcasted to both ```{"allow-access": true}```
    - Players get redirected to /desk-table in the page

 * Desk Table:
  - Where game is developped. Players receive cards and exchange information with the proccessing of `GameDesk` as a middleware
