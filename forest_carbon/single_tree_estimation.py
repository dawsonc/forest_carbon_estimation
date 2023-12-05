"""
Implementing the allometric model to estimate the aboveground biomass of a tree based
on the paper "Improved allometric models to estimate the aboveground biomass of tropical
trees" by Chave et. al.
"""

import math
from typing import Callable

from beartype import beartype

AGBModel = Callable[[float, float, float], float]


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


@beartype
def create_AGB_function_no_height(
    const: float, coef_e: float, coef_rho: float, coef_d: float, coef_d_squared: float
) -> AGBModel:
    """
    Returns a function that takes in the parameters rho, d, and e and outputs the
    estimated AGB.
    The model is in an exponential form: AGB = coef * (rho * d^2 * h) ^ exp.

    Arguments:
    const (float),
    coef_e (float),
    coef_rho (float),
    coef_d (float),
    coef_d_squared (float)
     the parameters that were fitted to the exponential AGB model.
    """

    def AGB_function(rho, d, e):
        return math.exp(
            const
            - coef_e * e
            + coef_rho * math.log(rho)
            + coef_d * math.log(d)
            - coef_d_squared * math.log(d**2)
        )

    return AGB_function


@beartype
def apply_AGB_model_no_height(agb: AGBModel, rho: float, d: float, e: float) -> float:
    """
    Returns the estimate for the AGB given a model to apply (agb), rho, d, and e.

    Arguments:
    rho (float): wood specific gravity (g/cm^3)
    d (float): trunk diameter (cm)
    e (float): environmental stressor
    """
    return agb(rho, d, e)
