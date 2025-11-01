"""Example: Monte Carlo option pricing with GPU acceleration."""
from __future__ import annotations

import numpy as np
from core import KernelBase, Config, PrecisionMode, Backend


class MonteCarloOptionPricer(KernelBase):
    """GPU-accelerated Monte Carlo engine for option pricing."""
    
    def __init__(self, config: Config | None = None):
        super().__init__(config)
    
    def execute(
        self,
        spot: float,
        strike: float,
        rate: float,
        volatility: float,
        maturity: float,
        n_paths: int = 100_000,
        option_type: str = "call"
    ) -> dict:
        """
        Price European option using Monte Carlo simulation.
        
        Args:
            spot: Current asset price
            strike: Strike price
            rate: Risk-free rate
            volatility: Volatility (annualized)
            maturity: Time to maturity (years)
            n_paths: Number of simulation paths
            option_type: "call" or "put"
        
        Returns:
            Pricing results with statistics
        """
        # Generate random normal samples
        Z = np.random.randn(n_paths)
        
        # Simulate final asset prices (geometric Brownian motion)
        drift = (rate - 0.5 * volatility**2) * maturity
        diffusion = volatility * np.sqrt(maturity) * Z
        final_prices = spot * np.exp(drift + diffusion)
        
        # Calculate payoffs
        if option_type.lower() == "call":
            payoffs = np.maximum(final_prices - strike, 0.0)
        else:  # put
            payoffs = np.maximum(strike - final_prices, 0.0)
        
        # Discount to present value
        discount_factor = np.exp(-rate * maturity)
        discounted_payoffs = payoffs * discount_factor
        
        # Calculate price and statistics
        option_price = np.mean(discounted_payoffs)
        std_error = np.std(discounted_payoffs) / np.sqrt(n_paths)
        
        # Update telemetry
        self._telemetry['paths_simulated'] = n_paths
        self._telemetry['convergence_rate'] = std_error / option_price if option_price > 0 else 0.0
        
        return {
            'price': option_price,
            'std_error': std_error,
            'confidence_95': (
                option_price - 1.96 * std_error,
                option_price + 1.96 * std_error
            ),
            'in_the_money_pct': np.mean(payoffs > 0) * 100,
            'average_payoff': np.mean(payoffs),
            'max_payoff': np.max(payoffs)
        }


def example_option_pricing():
    """Price a European call option using Monte Carlo."""
    # Market parameters
    spot = 100.0
    strike = 105.0
    rate = 0.05
    volatility = 0.2
    maturity = 1.0
    
    # Configure for GPU execution with high precision
    config = Config(
        precision=PrecisionMode.FP64,
        backend=Backend.CUDA,
        enable_telemetry=True
    )
    
    # Price the option
    pricer = MonteCarloOptionPricer(config)
    result = pricer.execute(
        spot=spot,
        strike=strike,
        rate=rate,
        volatility=volatility,
        maturity=maturity,
        n_paths=1_000_000,
        option_type="call"
    )
    
    print(f"Monte Carlo Option Pricing Results")
    print(f"===================================")
    print(f"Option Price: ${result['price']:.4f}")
    print(f"Std Error: ${result['std_error']:.4f}")
    print(f"95% CI: (${result['confidence_95'][0]:.4f}, ${result['confidence_95'][1]:.4f})")
    print(f"In-the-money: {result['in_the_money_pct']:.2f}%")
    print(f"Average Payoff: ${result['average_payoff']:.4f}")
    print(f"Max Payoff: ${result['max_payoff']:.4f}")
    print(f"\nTelemetry:")
    print(f"  Paths simulated: {pricer.telemetry['paths_simulated']:,}")
    print(f"  Convergence rate: {pricer.telemetry['convergence_rate']:.6f}")
    
    return result


if __name__ == "__main__":
    example_option_pricing()
