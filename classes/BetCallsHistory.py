from constants.bets import *
class BetCallsHistory:
    def __init__(self) -> None:
        self.truco_calls = _TrucoCallsHistory()
        self.envido_calls = _EnvidoCallsHistory() 
    def upgrade_call(self, bet:list[str]):
         if bet[0] == ENVIDO:
              if bet[1] == ENVIDO: self.envido_calls.envido += 1
              if bet[1] == REAL_ENVIDO: self.envido_calls.real_envido += 1
              if bet[1] == FALTA_ENVIDO: self.envido_calls.falta_envido += 1
         elif bet[0] == TRUCO:
              if bet[1] == TRUCO: self.truco_calls.truco += 1
              if bet[1] == RE_TRUCO: self.truco_calls.re_truco += 1
              if bet[1] == VALE_CUATRO: self.truco_calls.vale_cuatro += 1

class _TrucoCallsHistory:
        def __init__(self) -> None:
            self.truco: int = 0 
            self.re_truco: int = 0
            self.vale_cuatro: int = 0
class _EnvidoCallsHistory:
    def __init__(self) -> None:
        self.envido: int = 0
        self.real_envido: int = 0
        self.falta_envido: int = 0
