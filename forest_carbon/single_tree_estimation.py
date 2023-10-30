"""
Implementing the allometric model in the paper "Improved allometric models to estimate
the aboveground biomass of tropical trees" by Chave et. al.
"""

import math


def find_sigma(N, p, e):
    """
    Returns the RSE for a model given the following arguments.
    N: sample size
    p: number of parameters
    e: array containing the error for each sample
    """
    square_sum = 0
    for error in e:
        square_sum += error**2
    return math.sqrt(1 / (N - p) * square_sum)


def create_AGB_function(alpha, beta, sigma, sigmap):
    """
    Returns a function that takes in the parameters rho, d, and h and outputs the
    estimated AGB.

    Arguments:
    alpha, beta: model coefficients derived from least squares regression
    sigma: residual standard error (RSE)
    sigmap: TODO
    """

    def AGB_function(rho, d, h):
        return math.exp(
            sigma**2 / 2
            + (beta**2) * (sigmap**2) / 2
            + alpha
            + beta * math.log(rho * d**2)
            + beta * math.log(h)
        )

    return AGB_function


def apply_AGB_model(agb, rho, d, h):
    """
    Returns the estimate for the AGB given a model to apply (agb), rho, d, and h.
    """
    return agb(rho, d, h)
