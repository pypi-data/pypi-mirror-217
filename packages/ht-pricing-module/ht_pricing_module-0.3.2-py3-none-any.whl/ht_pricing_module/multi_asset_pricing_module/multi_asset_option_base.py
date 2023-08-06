from ..monte_carlo_engine import *
from ..api_and_utils import *


class MultiAssetOptionBase:

    def __init__(self, param):
        self.param = Params(param) if isinstance(param, dict) else param

    def __calculate_present_value__(self) -> float:
        raise NotImplementedError()

    @lru_cache(maxsize=10)
    def present_value(self) -> float:
        return self.__calculate_present_value__()

    @lru_cache(maxsize=10)
    def delta(self, leg: int, step: float = 0.001) -> float:
        spot_price = f'spot_price{leg}'
        time_to_expiry = (self.param.expiry_date - self.param.current_date) / self.param.year_base
        if time_to_expiry <= 0:
            return 0.0

        if hasattr(self.param, spot_price):
            spot_up = getattr(self.param, spot_price) * (1 + step)
            spot_down = getattr(self.param, spot_price) * (1 - step)
            pricer_up = deepcopy(self)
            setattr(pricer_up.param, spot_price, spot_up)
            pricer_down = deepcopy(self)
            setattr(pricer_down.param, spot_price, spot_down)
            return (pricer_up.present_value() - pricer_down.present_value()) / (spot_up - spot_down)
        return 0.0

    @lru_cache(maxsize=10)
    def gamma(self, leg: int, step: float = 0.001) -> float:
        spot_price = f'spot_price{leg}'
        if hasattr(self.param, spot_price):
            spot_up = getattr(self.param, spot_price) * (1 + step)
            spot_down = getattr(self.param, spot_price) * (1 - step)
            pricer_up = deepcopy(self)
            setattr(pricer_up.param, spot_price, spot_up)
            pricer_down = deepcopy(self)
            setattr(pricer_down.param, spot_price, spot_down)
            return (pricer_up.present_value() + pricer_down.present_value() - 2 * self.present_value()) / pow((spot_up - spot_down) / 2, 2) 
        return 0.0

    @lru_cache(maxsize=10)
    def vega(self, leg: int, step: float = 0.01) -> float:
        volatility = f'volatility{leg}'
        if hasattr(self.param, volatility):
            vol_up = getattr(self.param, volatility) + step
            pricer_up = deepcopy(self)
            setattr(pricer_up.param, volatility, vol_up)
            return pricer_up.present_value() - self.present_value()
        return 0.0

    @lru_cache(maxsize=10)
    def theta(self, step: float = 1) -> float:
        if hasattr(self.param, 'current_date'):
            current_up = self.param.current_date + step
            pricer_up = deepcopy(self)
            pricer_up.param.current_date = current_up
            return pricer_up.present_value() - self.present_value()
        return 0.0

    @lru_cache(maxsize=10)
    def rho(self, step: float = 0.0001) -> float:
        if hasattr(self.param, 'riskfree_rate'):
            current_up = self.param.riskfree_rate + step
            pricer_up = deepcopy(self)
            pricer_up.param.riskfree_rate = current_up
            return pricer_up.present_value() - self.present_value()
        return 0.0

    @lru_cache(maxsize=10)
    def dpvdcorr(self, step: float = 0.01) -> float:
        if hasattr(self.param, 'correlation'):
            corr_up = self.param.correlation + step
            corr_down = self.param.correlation - step
            pricer_up = deepcopy(self)
            pricer_up.param.correlation = corr_up
            pricer_down = deepcopy(self)
            pricer_down.param.correlation = corr_down
            return (pricer_up.present_value() - pricer_down.present_value()) / 2
        return 0.0

    @lru_cache(maxsize=10)
    def ddeltadt(self, leg: int, time_step: float = 1, price_step: float = 0.001):
        if hasattr(self.param, 'current_date'):
            current_up = self.param.current_date + time_step
            pricer_up = deepcopy(self)
            pricer_up.param.current_date = current_up
            return pricer_up.delta(leg=leg, step=price_step) - self.delta(leg=leg, step=price_step)
        return 0.0

    @lru_cache(maxsize=10)
    def ddeltadv(self, leg: int, vol_step: float = 0.01, price_step: float = 0.001):
        volatility = f'volatility{leg}'
        if hasattr(self.param, volatility):
            vol_up = getattr(self.param, volatility) + vol_step
            pricer_up = deepcopy(self)
            setattr(pricer_up.param, volatility, vol_up)
            return pricer_up.delta(leg=leg, step=price_step) - self.delta(leg=leg, step=price_step)
        return 0.0
