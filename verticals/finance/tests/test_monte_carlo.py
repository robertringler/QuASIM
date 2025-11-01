"""Tests for Monte Carlo option pricing."""
from __future__ import annotations

import pytest
from core import Config, PrecisionMode, Backend


def test_monte_carlo_import():
    """Test that we can import the Monte Carlo pricer."""
    from verticals.finance.examples.monte_carlo_pricing import MonteCarloOptionPricer
    assert MonteCarloOptionPricer is not None


def test_call_option_pricing():
    """Test call option pricing with known parameters."""
    from verticals.finance.examples.monte_carlo_pricing import MonteCarloOptionPricer
    
    config = Config(precision=PrecisionMode.FP64, backend=Backend.CPU)
    pricer = MonteCarloOptionPricer(config)
    
    result = pricer.execute(
        spot=100.0,
        strike=100.0,
        rate=0.05,
        volatility=0.2,
        maturity=1.0,
        n_paths=10_000,
        option_type="call"
    )
    
    # At-the-money call option should have positive value
    assert result['price'] > 0
    assert result['std_error'] > 0
    assert result['price'] > result['std_error']  # Price should be significant
    
    # Confidence interval should contain the price
    ci_lower, ci_upper = result['confidence_95']
    assert ci_lower <= result['price'] <= ci_upper


def test_put_option_pricing():
    """Test put option pricing."""
    from verticals.finance.examples.monte_carlo_pricing import MonteCarloOptionPricer
    
    pricer = MonteCarloOptionPricer()
    result = pricer.execute(
        spot=100.0,
        strike=100.0,
        rate=0.05,
        volatility=0.2,
        maturity=1.0,
        n_paths=10_000,
        option_type="put"
    )
    
    # At-the-money put option should have positive value
    assert result['price'] > 0
    assert result['in_the_money_pct'] > 0


def test_deep_otm_call():
    """Test that deep out-of-the-money call has low value."""
    from verticals.finance.examples.monte_carlo_pricing import MonteCarloOptionPricer
    
    pricer = MonteCarloOptionPricer()
    result = pricer.execute(
        spot=100.0,
        strike=150.0,  # Deep OTM
        rate=0.05,
        volatility=0.2,
        maturity=1.0,
        n_paths=10_000,
        option_type="call"
    )
    
    # Deep OTM option should have low value
    assert result['price'] < 10.0
    assert result['in_the_money_pct'] < 50.0


def test_telemetry():
    """Test that telemetry is captured."""
    from verticals.finance.examples.monte_carlo_pricing import MonteCarloOptionPricer
    
    config = Config(enable_telemetry=True)
    pricer = MonteCarloOptionPricer(config)
    
    pricer.execute(
        spot=100.0, strike=100.0, rate=0.05,
        volatility=0.2, maturity=1.0, n_paths=1000
    )
    
    assert 'paths_simulated' in pricer.telemetry
    assert pricer.telemetry['paths_simulated'] == 1000
    assert 'convergence_rate' in pricer.telemetry


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
