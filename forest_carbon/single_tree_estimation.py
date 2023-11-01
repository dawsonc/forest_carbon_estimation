"""
Implementing the allometric model to estimate the aboveground biomass of a tree based
on the paper "Improved allometric models to estimate the aboveground biomass of tropical
trees" by Chave et. al.
"""


def create_AGB_function(coef, exp):
    """
    Returns a function that takes in the parameters rho, d, and h and outputs the
    estimated AGB.

    Arguments:
    coef, exp: the parameters that were fitted to the exponential AGB model.
    """

    def AGB_function(rho, d, h):
        return coef * (rho * d**2 * h) ** exp

    return AGB_function


def apply_AGB_model(agb, rho, d, h):
    """
    Returns the estimate for the AGB given a model to apply (agb), rho, d, and h.

    Arguments:
    rho: wood specific gravity (g/cm^3)
    d: trunk diameter (cm)
    h: total tree height (m)
    """
    return agb(rho, d, h)
