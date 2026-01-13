from constants.bets import *
class BetCallsHistory:
    def __init__(self) -> None:
        self.truco: int = 0 
        self.re_truco: int = 0
        self.vale_cuatro: int = 0
        self.envido: int = 0
        self.real_envido: int = 0
        self.falta_envido: int = 0
        self._bet_values: dict[str, int] = {
            ENVIDO: 2,
            REAL_ENVIDO:3,
            # 'falta_envido': 0 Updates dinamically
            TRUCO: 2,
            RE_TRUCO: 3,
            VALE_CUATRO: 4
        }
        self.last_bet_accepted: bool = False
        self.in_bet: bool = False
        self.was_envido_played: bool = False
        self.latest: list[str] = []
        self.latest_by_id: dict[int, str] = {0: '', 1: ''}
    def upgrade_call(self, bet:list[str]):
        if bet[0] == ENVIDO:
            if bet[1] == ENVIDO: self.envido += 1
            if bet[1] == REAL_ENVIDO: self.real_envido += 1
            if bet[1] == FALTA_ENVIDO: self.falta_envido += 1
            if bet[1] in FINAL_ANSWER: self.was_envido_played = True
            self._set_truco_bets_to_zero()
        if bet[1] == TRUCO: self.truco += 1
        if bet[1] == RE_TRUCO: self.re_truco += 1
        if bet[1] == VALE_CUATRO: self.vale_cuatro += 1
        self.latest = bet

    def return_envido_accepted_points(self) -> int:
        res: int = 0
        # if self.falta_envido: return res # Game desk handles this case appart
        if self.envido: res += self.envido * self._bet_values[ENVIDO] # Envido can be called twice
        if self.real_envido: res += self._bet_values[REAL_ENVIDO]
        return res
    def return_envido_not_accepted_points(self) -> int:
        if not (self.envido or self.real_envido or self.falta_envido): return 1

        return self.envido + self.real_envido + self.falta_envido
    
    def return_truco_accepted_points(self) -> int:
        # res: int = 0
        if self.vale_cuatro: return self._bet_values[VALE_CUATRO]
        if self.re_truco: return self._bet_values[RE_TRUCO]
        if self.truco: return self._bet_values[TRUCO]
        return 1
    
    def return_truco_not_accepted_points(self) -> int:
        return self.truco + self.re_truco + self.vale_cuatro


    def _set_truco_bets_to_zero(self):
        self.truco = 0
        self.re_truco = 0
        self.vale_cuatro = 0

