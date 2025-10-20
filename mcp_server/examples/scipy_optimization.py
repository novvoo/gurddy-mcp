"""
SciPy Integration Examples using Gurddy

This module demonstrates integration between Gurddy and SciPy for advanced optimization:
1. Nonlinear optimization using scipy.optimize
2. Statistical optimization problems
3. Signal processing optimization
4. Numerical integration in optimization
5. Hybrid CSP-SciPy approaches
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import numpy as np
import gurddy
from typing import Dict, List, Tuple, Optional

# Check if SciPy functionality is available through gurddy
try:
    # Test if SciPy integration is available
    from gurddy import ScipySolver
    SCIPY_AVAILABLE = True
except ImportError:
    print("Warning: SciPy integration not available. Install with: pip install scipy")
    SCIPY_AVAILABLE = False


def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def example_nonlinear_portfolio_optimization():
    """
    Portfolio optimization with nonlinear risk constraints using SciPy.
    Combines Gurddy's linear constraints with SciPy's nonlinear optimization.
    """
    if not SCIPY_AVAILABLE:
        print("SciPy not available - skipping nonlinear portfolio example")
        return
        
    print_section("Example 1: Nonlinear Portfolio Optimization with SciPy")
    
    print("\nProblem: Portfolio optimization with quadratic risk model")
    print("Assets: 4 stocks with expected returns and covariance matrix")
    
    # Asset data
    assets = ['AAPL', 'GOOGL', 'MSFT', 'TSLA']
    expected_returns = np.array([0.12, 0.15, 0.10, 0.18])
    
    # Covariance matrix (risk model)
    covariance_matrix = np.array([
        [0.04, 0.02, 0.01, 0.03],
        [0.02, 0.06, 0.02, 0.04],
        [0.01, 0.02, 0.03, 0.02],
        [0.03, 0.04, 0.02, 0.08]
    ])
    
    print(f"Expected returns: {expected_returns}")
    print(f"Covariance matrix shape: {covariance_matrix.shape}")
    
    # First, use Gurddy for linear constraints setup
    model = gurddy.Model("Portfolio_Linear", "LP")
    
    # Variables: portfolio weights
    weights = {}
    for i, asset in enumerate(assets):
        weights[asset] = model.addVar(f"w_{asset}", low_bound=0, up_bound=0.4, cat='Continuous')
    
    # Linear constraints using Gurddy
    # Constraint 1: weights sum to 1
    total_weight = sum(weights[asset] for asset in assets)
    model.addConstraint(total_weight == 1.0, name='FullyInvested')
    
    # Constraint 2: minimum diversification (at least 10% in each asset)
    for asset in assets:
        model.addConstraint(weights[asset] >= 0.1, name=f'MinWeight_{asset}')
    
    # Get feasible starting point from Gurddy
    # Simple equal-weight objective for initial solution
    model.setObjective(sum(weights[asset] for asset in assets), sense='Maximize')
    initial_solution = model.solve()
    
    if initial_solution:
        x0 = np.array([initial_solution[f"w_{asset}"] for asset in assets])
        print(f"Initial feasible solution: {x0}")
    else:
        x0 = np.array([0.25, 0.25, 0.25, 0.25])  # Equal weights fallback
        print(f"Using equal weights as starting point: {x0}")
    
    # Now use Gurddy's SciPy integration for nonlinear optimization
    print("\nOptimizing with Gurddy's SciPy integration...")
    
    # Use Gurddy's portfolio optimization function
    result = gurddy.optimize_portfolio(
        expected_returns=expected_returns,
        covariance_matrix=covariance_matrix,
        risk_free_rate=0.02,
        bounds=[(0.1, 0.4) for _ in range(len(assets))],
        constraints=[{'type': 'ineq', 'fun': lambda x: 0.4 - np.max(x)}]  # Max 40% per asset
    )
    
    if result['success']:
        optimal_weights = result['weights']
        
        print(f"\nOptimal Portfolio (Maximum Sharpe Ratio):")
        for i, asset in enumerate(assets):
            print(f"  {asset}: {optimal_weights[i]:.1%}")
        
        print(f"\nPortfolio Metrics:")
        print(f"  Expected Return: {result['expected_return']:.1%}")
        print(f"  Volatility (Std): {result['volatility']:.1%}")
        print(f"  Sharpe Ratio: {result['sharpe_ratio']:.3f}")
        print(f"  Optimization Status: {result['message']}")
    else:
        print(f"Optimization failed: {result['message']}")


def example_statistical_optimization():
    """
    Statistical parameter estimation using SciPy with Gurddy constraints.
    """
    if not SCIPY_AVAILABLE:
        print("SciPy not available - skipping statistical optimization example")
        return
        
    print_section("Example 2: Statistical Parameter Estimation")
    
    print("\nProblem: Fit distribution parameters with constraints")
    print("Fit a Gamma distribution to data with shape parameter constraints")
    
    # Generate synthetic data from known Weibull distribution
    np.random.seed(42)
    true_shape = 2.5
    true_scale = 1.8
    
    # Use numpy to generate Weibull data (equivalent to scipy.stats.weibull_min)
    data = np.random.weibull(true_shape, size=100) * true_scale
    
    print(f"True parameters: shape={true_shape}, scale={true_scale}")
    print(f"Data sample: mean={np.mean(data):.3f}, std={np.std(data):.3f}")
    
    print("\nApplying constraints: 1.5 ≤ shape ≤ 4.0, 1.0 ≤ scale ≤ 3.0")
    
    # Use Gurddy's distribution fitting function with gamma distribution
    result = gurddy.fit_distribution(
        data=data,
        distribution='gamma',
        bounds=[(1.5, 4.0), (1.0, 3.0)],  # shape, scale bounds
        method='mle'
    )
    
    if 'parameters' in result:
        params = result['parameters']
        print(f"Fitted parameters: {params}")
        if len(params) >= 2:
            print(f"  Shape: {params[0]:.3f}, Scale: {params[1]:.3f}")
        
        print(f"\nFitting Results:")
        print(f"  Log-likelihood: {result['log_likelihood']:.2f}")
        print(f"  AIC: {result['aic']:.2f}")
        
        print(f"\nKolmogorov-Smirnov test (higher p-value is better):")
        print(f"  KS statistic: {result['ks_statistic']:.4f}")
        print(f"  p-value: {result['p_value']:.4f}")
        print(f"  Fit quality: {'Good' if result['p_value'] > 0.05 else 'Poor'}")
    else:
        print("Distribution fitting failed")


def example_signal_processing_optimization():
    """
    Signal processing optimization using SciPy with Gurddy for discrete constraints.
    """
    if not SCIPY_AVAILABLE:
        print("SciPy not available - skipping signal processing example")
        return
        
    print_section("Example 3: Signal Processing Filter Design")
    
    print("\nProblem: Design FIR filter with discrete coefficient constraints")
    print("Optimize filter coefficients for desired frequency response")
    
    # Filter specifications
    fs = 1000  # Sampling frequency
    cutoff = 100  # Cutoff frequency
    num_taps = 21  # Filter length (odd for symmetric)
    
    print(f"Filter specs: fs={fs}Hz, cutoff={cutoff}Hz, taps={num_taps}")
    
    print("\nDesigning and optimizing FIR filter with Gurddy...")
    
    # Use Gurddy's filter design function
    result = gurddy.design_filter(
        num_taps=num_taps,
        cutoff_freq=cutoff,
        sampling_freq=fs,
        filter_type='lowpass',
        optimize=True
    )
    
    if 'coefficients' in result:
        optimized_filter = result['coefficients']
        initial_filter = result['initial_coefficients']
        
        print(f"\nFilter Design Results:")
        print(f"  Optimized: {result['optimized']}")
        if result['optimized']:
            print(f"  Improvement: {result['improvement']:.6f}")
        
        print(f"  Filter coefficients range: [{np.min(optimized_filter):.4f}, {np.max(optimized_filter):.4f}]")
        
        # Simple performance metrics
        print(f"  Number of coefficients: {len(optimized_filter)}")
        print(f"  Filter type: Lowpass FIR")
    else:
        print("Filter design failed")


def example_hybrid_csp_scipy():
    """
    Hybrid approach: Use Gurddy CSP for discrete decisions, SciPy for continuous optimization.
    """
    if not SCIPY_AVAILABLE:
        print("SciPy not available - skipping hybrid CSP-SciPy example")
        return
        
    print_section("Example 4: Hybrid CSP-SciPy Facility Location")
    
    print("\nProblem: Facility location with discrete site selection and continuous capacity")
    print("Step 1: Use Gurddy CSP to select facility locations")
    print("Step 2: Use SciPy to optimize continuous parameters (capacity, routing)")
    
    # Problem data
    num_facilities = 3
    num_customers = 5
    max_facilities = 2  # Budget constraint
    
    # Customer locations and demands
    customer_locations = np.array([
        [1, 2], [3, 4], [5, 1], [2, 5], [4, 3]
    ])
    customer_demands = np.array([10, 15, 8, 12, 20])
    
    # Potential facility locations
    facility_locations = np.array([
        [2, 3], [4, 2], [3, 4]
    ])
    
    print(f"Customers: {num_customers}, Potential facilities: {num_facilities}")
    print(f"Budget: max {max_facilities} facilities")
    
    # Step 1: CSP for facility selection
    print("\nStep 1: Solving facility selection with Gurddy CSP...")
    
    model = gurddy.Model("FacilitySelection", "CSP")
    
    # Binary variables: facility i is selected or not
    facility_vars = {}
    for i in range(num_facilities):
        facility_vars[i] = model.addVar(f"facility_{i}", domain=[0, 1])
    
    # Constraint: select at most max_facilities
    def budget_constraint(*facilities):
        return sum(facilities) <= max_facilities
    
    model.addConstraint(gurddy.FunctionConstraint(
        budget_constraint, tuple(facility_vars.values())
    ))
    
    # Constraint: at least one facility must be selected
    def min_facilities_constraint(*facilities):
        return sum(facilities) >= 1
    
    model.addConstraint(gurddy.FunctionConstraint(
        min_facilities_constraint, tuple(facility_vars.values())
    ))
    
    # Solve CSP
    csp_solution = model.solve()
    
    if csp_solution:
        selected_facilities = [i for i in range(num_facilities) 
                             if csp_solution[f"facility_{i}"] == 1]
        print(f"Selected facilities: {selected_facilities}")
        
        if not selected_facilities:
            print("No facilities selected - using fallback selection")
            selected_facilities = [0, 1]  # Fallback to first two facilities
        
        # Step 2: Continuous optimization with Gurddy's SciPy integration
        print("\nStep 2: Optimizing capacities and routing with Gurddy's SciPy integration...")
        
        n_selected = len(selected_facilities)
        selected_locations = facility_locations[selected_facilities]
        
        # Calculate distances
        distances = np.zeros((n_selected, num_customers))
        for i, fac_idx in enumerate(selected_facilities):
            for j in range(num_customers):
                distances[i, j] = np.linalg.norm(
                    facility_locations[fac_idx] - customer_locations[j]
                )
        
        print(f"Distance matrix shape: {distances.shape}")
        
        def continuous_objective(x_continuous, discrete_solution):
            """Minimize total transportation cost + facility cost"""
            # x_continuous contains: [capacities (n_selected), routing (n_selected * num_customers)]
            capacities = x_continuous[:n_selected]
            routing = x_continuous[n_selected:].reshape(n_selected, num_customers)
            
            # Transportation cost
            transport_cost = np.sum(distances * routing)
            
            # Facility fixed costs (proportional to capacity)
            facility_cost = np.sum(capacities * 100)  # $100 per unit capacity
            
            # Penalty for unmet demand
            total_served = np.sum(routing, axis=0)
            unmet_demand = np.maximum(0, customer_demands - total_served)
            penalty = np.sum(unmet_demand * 1000)  # High penalty
            
            return transport_cost + facility_cost + penalty
        
        # Define continuous variables
        continuous_vars = []
        for i in range(n_selected):
            continuous_vars.append(f"capacity_{i}")
        for i in range(n_selected):
            for j in range(num_customers):
                continuous_vars.append(f"route_{i}_{j}")
        
        # Initial guess
        total_demand = np.sum(customer_demands)
        x0 = np.zeros(len(continuous_vars))
        
        # Initial capacities (equal split of total demand)
        if n_selected > 0:
            x0[:n_selected] = total_demand / n_selected
        else:
            print("Error: No facilities selected")
            return
        
        # Bounds for continuous variables
        bounds = []
        # Capacity bounds
        for i in range(n_selected):
            bounds.append((0, total_demand))
        # Routing bounds
        for i in range(n_selected):
            for j in range(num_customers):
                bounds.append((0, customer_demands[j]))
        
        # Use Gurddy's hybrid solver
        solver = gurddy.ScipySolver()
        result = solver.solve_hybrid_problem(
            discrete_model=model,
            continuous_objective=continuous_objective,
            continuous_variables=continuous_vars,
            x0=x0,
            bounds=bounds
        )
        
        if result['success']:
            continuous_solution = result['continuous_solution']
            
            # Extract capacities and routing
            optimal_capacities = []
            optimal_routing = np.zeros((n_selected, num_customers))
            
            for i in range(n_selected):
                optimal_capacities.append(continuous_solution[f"capacity_{i}"])
            
            for i in range(n_selected):
                for j in range(num_customers):
                    optimal_routing[i, j] = continuous_solution[f"route_{i}_{j}"]
            
            print(f"\nOptimal Hybrid Solution:")
            print(f"Facility capacities: {optimal_capacities}")
            print(f"Total cost: ${result['objective_value']:.2f}")
            
            print(f"\nRouting matrix (facility -> customer):")
            for i, fac_idx in enumerate(selected_facilities):
                print(f"  Facility {fac_idx}: {optimal_routing[i, :]}")
            
            # Verify demand satisfaction
            total_served = np.sum(optimal_routing, axis=0)
            print(f"\nDemand satisfaction:")
            for j in range(num_customers):
                print(f"  Customer {j}: demand={customer_demands[j]:.1f}, served={total_served[j]:.1f}")
        
        else:
            print(f"Hybrid optimization failed: {result['message']}")
    
    else:
        print("CSP failed to find facility selection solution")
        print("Using fallback facility selection: [0, 1]")
        selected_facilities = [0, 1]
        
        # Continue with SciPy optimization using fallback selection
        n_selected = len(selected_facilities)
        selected_locations = facility_locations[selected_facilities]
        
        # Calculate distances
        distances = np.zeros((n_selected, num_customers))
        for i, fac_idx in enumerate(selected_facilities):
            for j in range(num_customers):
                distances[i, j] = np.linalg.norm(
                    facility_locations[fac_idx] - customer_locations[j]
                )
        
        print(f"Fallback solution - using facilities {selected_facilities}")
        print(f"Distance matrix shape: {distances.shape}")


def example_numerical_integration_optimization():
    """
    Optimization involving numerical integration using SciPy.
    """
    if not SCIPY_AVAILABLE:
        print("SciPy not available - skipping numerical integration example")
        return
        
    print_section("Example 5: Optimization with Numerical Integration")
    
    print("\nProblem: Optimize parameters of a probability distribution")
    print("Minimize difference between theoretical and empirical quantiles")
    
    # Generate sample data from known distribution
    np.random.seed(42)
    true_params = [2.0, 1.5]  # shape, scale for gamma distribution
    
    # Generate gamma-distributed data using numpy
    sample_data = np.random.gamma(true_params[0], true_params[1], size=200)
    
    print(f"True parameters: shape={true_params[0]}, scale={true_params[1]}")
    print(f"Sample statistics: mean={np.mean(sample_data):.3f}, std={np.std(sample_data):.3f}")
    
    # Empirical quantiles
    quantile_levels = np.array([0.1, 0.25, 0.5, 0.75, 0.9])
    empirical_quantiles = np.quantile(sample_data, quantile_levels)
    
    print(f"Empirical quantiles: {empirical_quantiles}")
    
    print("\nFitting distribution parameters with Gurddy...")
    
    # Use both MLE and quantile methods
    result_mle = gurddy.fit_distribution(
        data=sample_data,
        distribution='gamma',
        bounds=[(0.1, 10.0), (0.1, 10.0)],  # shape, scale bounds
        method='mle'
    )
    
    result_quantile = gurddy.fit_distribution(
        data=sample_data,
        distribution='gamma',
        bounds=[(0.1, 10.0), (0.1, 10.0)],
        method='quantile'
    )
    
    print(f"\nMLE Fitting Results:")
    if 'parameters' in result_mle:
        estimated_params_mle = result_mle['parameters']
        print(f"  Estimated parameters: shape={estimated_params_mle[0]:.3f}, scale={estimated_params_mle[1]:.3f}")
        print(f"  Parameter errors: shape={abs(estimated_params_mle[0] - true_params[0]):.3f}, "
              f"scale={abs(estimated_params_mle[1] - true_params[1]):.3f}")
        print(f"  Log-likelihood: {result_mle['log_likelihood']:.2f}")
        print(f"  AIC: {result_mle['aic']:.2f}")
        print(f"  KS test p-value: {result_mle['p_value']:.4f}")
    
    print(f"\nQuantile Matching Results:")
    if 'parameters' in result_quantile:
        estimated_params_quantile = result_quantile['parameters']
        print(f"  Estimated parameters: shape={estimated_params_quantile[0]:.3f}, scale={estimated_params_quantile[1]:.3f}")
        print(f"  Parameter errors: shape={abs(estimated_params_quantile[0] - true_params[0]):.3f}, "
              f"scale={abs(estimated_params_quantile[1] - true_params[1]):.3f}")
        print(f"  Log-likelihood: {result_quantile['log_likelihood']:.2f}")
        print(f"  AIC: {result_quantile['aic']:.2f}")
        print(f"  KS test p-value: {result_quantile['p_value']:.4f}")
    
    # Compare methods
    print(f"\nMethod Comparison:")
    if 'parameters' in result_mle and 'parameters' in result_quantile:
        print(f"  MLE method: AIC={result_mle['aic']:.2f}, p-value={result_mle['p_value']:.4f}")
        print(f"  Quantile method: AIC={result_quantile['aic']:.2f}, p-value={result_quantile['p_value']:.4f}")
        
        better_method = "MLE" if result_mle['aic'] < result_quantile['aic'] else "Quantile"
        print(f"  Better method (lower AIC): {better_method}")


def main():
    """Run all SciPy integration examples"""
    if not SCIPY_AVAILABLE:
        print("SciPy is not installed. Please install it with:")
        print("  pip install scipy")
        print("  or")
        print("  pip install gurddy[scipy]")
        return
    
    print("\n" + "=" * 70)
    print("  GURDDY + SCIPY INTEGRATION EXAMPLES")
    print("=" * 70)
    print("\nDemonstrating advanced optimization by combining Gurddy's")
    print("constraint satisfaction with SciPy's numerical optimization.")
    
    # Run all examples
    example_nonlinear_portfolio_optimization()
    example_statistical_optimization()
    example_signal_processing_optimization()
    example_hybrid_csp_scipy()
    example_numerical_integration_optimization()
    
    print("\n" + "=" * 70)
    print("  ALL SCIPY INTEGRATION EXAMPLES COMPLETED")
    print("=" * 70)
    print("\nKey Integration Benefits:")
    print("  • Gurddy handles discrete constraints and feasibility")
    print("  • SciPy provides advanced nonlinear optimization")
    print("  • Hybrid approaches solve complex real-world problems")
    print("  • Statistical and signal processing applications")
    print("  • Numerical integration in optimization objectives")
    print("\n")


if __name__ == "__main__":
    main()