"""
Implementing the allometric model to estimate the aboveground biomass of a tree based
on the paper "Improved allometric models to estimate the aboveground biomass of tropical
trees" by Chave et. al.
"""

from beartype import beartype
from beartype.typing import Callable, TypeAlias

AGBModel: TypeAlias = Callable[[float, float, float], float]


@beartype
def create_AGB_function(coef: float, exp: float) -> AGBModel:
    """
    Returns a function that takes in the parameters rho, d, and h and outputs the
    estimated AGB.
    The model is in an exponential form: AGB = coef * (rho * d^2 * h) ^ exp.

    Arguments:
    coef (float), exp (float): the parameters that were fitted to the exponential AGB model.
    """

    def AGB_function(rho, d, h):
        return coef * (rho * d**2 * h) ** exp

    return AGB_function


@beartype
def apply_AGB_model(agb: AGBModel, rho: float, d: float, h: float) -> float:
    """
    Returns the estimate for the AGB given a model to apply (agb), rho, d, and h.

    Arguments:
    rho (float): wood specific gravity (g/cm^3)
    d (float): trunk diameter (cm)
    h (float): total tree height (m)
    """
    return agb(rho, d, h)
