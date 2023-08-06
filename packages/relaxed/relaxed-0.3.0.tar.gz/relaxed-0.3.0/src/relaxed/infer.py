"""Calculate expected CLs values with hypothesis tests."""
from __future__ import annotations

__all__ = ("hypotest",)

import logging
from typing import Any

import jax.numpy as jnp
import pyhf
from equinox import filter_jit
from jax import Array

from relaxed.mle import fit, fixed_poi_fit

PyTree = Any


@filter_jit
def hypotest(
    test_poi: float,
    data: Array,
    model: PyTree,
    return_mle_pars: bool = False,
    test_stat: str = "q",
    expected_pars: Array | None = None,
    cls_method: bool = True,
) -> tuple[Array, Array] | Array:
    """Calculate expected CLs/p-values via hypothesis tests.

    Parameters
    ----------
    test_poi : float
        The value of the test parameter to use for the hypothesis test.
    data : Array
        The data to use for the hypothesis test.
    model : pyhf.Model
        The model to use for the hypothesis test.
    lr : float
        Learning rate for the MLE fit, done via gradient descent.
    return_mle_pars : bool, optional
        Whether to return the MLE parameters calculated as a by-product.
    test_stat : str, optional
        The test statistic to use for the hypothesis test. One of:
        - "qmu" (default, used for upper limits)
        - "q0" (used for discovery of a positive signal)
    expected_pars : Array, optional
        Use if calculating expected significance and these are known. If not
        provided, the MLE parameters will be fitted.

    Returns
    -------
    Array
        The expected CLs/p-value.
    Array
        The MLE parameters, if `return_mle_pars` is True.
    """
    if test_stat == "q":
        return qmu_test(
            test_poi, data, model, return_mle_pars, expected_pars, cls_method
        )
    if test_stat == "q0":
        logging.info(
            "test_poi automatically set to 0 for q0 test (bkg-only null hypothesis)"
        )
        return q0_test(0.0, data, model, return_mle_pars, expected_pars)

    msg = f"Unknown test statistic: {test_stat}"
    raise ValueError(msg)


@filter_jit
def qmu_test(
    test_poi: float,
    data: Array,
    model: PyTree,
    return_mle_pars: bool = False,
    expected_pars: Array | None = None,
    cls_method: bool = True,
) -> tuple[Array, Array] | Array:
    # hard-code 1 as inits for now
    # TODO: need to parse different inits for constrained and global fits
    # because init_pars[0] is not necessarily the poi init
    init_pars = jnp.asarray(model.config.suggested_init())
    conditional_pars = fixed_poi_fit(
        data, model, poi_condition=test_poi, init_pars=init_pars[:-1]
    )
    if expected_pars is None:
        mle_pars = fit(data, model, init_pars=init_pars)
    else:
        mle_pars = expected_pars
    profile_likelihood = -2 * (
        model.logpdf(conditional_pars, data)[0] - model.logpdf(mle_pars, data)[0]
    )

    poi_hat = mle_pars[model.config.poi_index]
    qmu = jnp.where(poi_hat < test_poi, profile_likelihood, 0.0)

    CLsb = 1 - pyhf.tensorlib.normal_cdf(jnp.sqrt(qmu))
    if cls_method:
        altval = 0.0
        CLb = 1 - pyhf.tensorlib.normal_cdf(altval)
        CLs = CLsb / CLb
    else:
        CLs = CLsb
    return (CLs, mle_pars) if return_mle_pars else CLs


@filter_jit
def q0_test(
    test_poi: float,
    data: Array,
    model: PyTree,
    return_mle_pars: bool = False,
    expected_pars: Array | None = None,
) -> tuple[Array, Array] | Array:
    # hard-code 1 as inits for now
    # TODO: need to parse different inits for constrained and global fits
    # because init_pars[0] is not necessarily the poi init
    init_pars = jnp.asarray(model.config.suggested_init())
    conditional_pars = fixed_poi_fit(
        data,
        model,
        poi_condition=test_poi,
        init_pars=init_pars[:-1],
    )
    if expected_pars is None:
        mle_pars = fit(data, model, init_pars=init_pars)
    else:
        mle_pars = expected_pars
    profile_likelihood = -2 * (
        model.logpdf(conditional_pars, data)[0] - model.logpdf(mle_pars, data)[0]
    )

    poi_hat = mle_pars[model.config.poi_index]
    q0 = jnp.where(poi_hat >= test_poi, profile_likelihood, 0.0)
    p0 = 1 - pyhf.tensorlib.normal_cdf(jnp.sqrt(q0))

    return (p0, mle_pars) if return_mle_pars else p0
