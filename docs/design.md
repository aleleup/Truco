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
    player_0: Player;
    player_1: Player;
    deck: seq[Card];
    is_game_over: bool;
    hand: int;
    betting_points: int;


    def innit_game() -> None

    def start_new_row():

```
