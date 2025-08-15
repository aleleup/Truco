from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PlaygroundTable(Base):
    __tablename__ = "playground_table"
    id = Column(Integer, primary_key=True, index=True)
    playground_id = Column(Integer, unique=True, index=True)

    #TODO: search if table can have methdos


class GameTableTable(Base):
    '''game table -> table that contains data && game table -> table where players sit'''

    __tablename__ = "game_table"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String) # belongs in [ongoing, finished]
    winner_id = Column(Integer, nullable=True)
    player_0_points = Column(Integer)
    player_1_points = Column(Integer)



class CardRoundsTable(Base):

    __tablename__ = 'card_rounds'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String)
    envido_winner = Column(Integer)
    envido_points = Column(Integer)
    truco_winner = Column(Integer, nullable=False)
    truco_points = Column(Integer, nullable=False)
    player_0_cards = Column(String)    
    player_1_cards = Column(String)

class PlayersMoovemntsTable(Base):
    __tablename__ = 'players_movements'
    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer)
    is_bet = Column(Boolean)
    moovement = Column(String)