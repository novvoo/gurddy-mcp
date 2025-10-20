"""
Advanced LP Techniques using Gurddy

This example demonstrates:
1. Portfolio optimization problem
2. Multi-objective optimization
3. Constraint relaxation analysis
4. Performance comparison between different problem formulations
"""

import time
import gurddy
from typing import Dict, List, Tuple


def portfolio_optimization_example():
    """Solve a portfolio optimization problem using Gurddy."""
    print("=== Portfolio Optimization Problem ===")
    
    # Investment data: expected returns and risks
    assets = ['Stock_A', 'Stock_B', 'Stock_C', 'Bond_X', 'Bond_Y']
    expected_returns = {'Stock_A': 0.12, 'Stock_B': 0.10, 'Stock_C': 0.15, 'Bond_X': 0.05, 'Bond_Y': 0.06}
    risks = {'Stock_A': 0.20, 'Stock_B': 0.15, 'Stock_C': 0.25, 'Bond_X': 0.02, 'Bond_Y': 0.03}
    
    # Correlation matrix (simplified - assume some correlations)
    correlations = {
        ('Stock_A', 'Stock_B'): 0.6,
        ('Stock_A', 'Stock_C'): 0.4,
        ('Stock_B', 'Stock_C'): 0.5,
        # Bonds are less correlated with stocks
        ('Stock_A', 'Bond_X'): -0.1,
        ('Stock_A', 'Bond_Y'): -0.1,
        ('Stock_B', 'Bond_X'): -0.1,
        ('Stock_B', 'Bond_Y'): -0.1,
        ('Stock_C', 'Bond_X'): -0.1,
        ('Stock_C', 'Bond_Y'): -0.1,
        ('Bond_X', 'Bond_Y'): 0.8,
    }
    
    print(f"Assets: {assets}")
    print(f"Expected returns: {expected_returns}")
    print(f"Risk levels: {risks}")
    print()
    
    # Solve for maximum return portfolio
    model = gurddy.Model("MaxReturn_Portfolio", "LP")
    
    # Variables: allocation weights (must sum to 1)
    weights = {}
    for asset in assets:
        weights[asset] = model.addVar(f"w_{asset}", low_bound=0, up_bound=1, cat='Continuous')
    
    # Simple equal-weight objective for initial solution
    model.setObjective(sum(weights[asset] for asset in assets), sense='Maximize')
    
    # Constraint 1: weights sum to 1 (fully invested)
    total_weight = sum(weights[asset] for asset in assets)
    model.addConstraint(total_weight == 1.0, name='FullyInvested')
    
    # Constraint 2: risk limit (simplified risk measure)
    total_risk = sum(weights[asset] * risks[asset] for asset in assets)
    model.addConstraint(total_risk <= 0.12, name='RiskLimit')  # Max 12% risk
    
    # Constraint 3: diversification - no single asset > 40%
    for asset in assets:
        model.addConstraint(weights[asset] <= 0.4, name=f'Diversify_{asset}')
    
    # Constraint 4: minimum bond allocation (conservative requirement)
    bond_allocation = weights['Bond_X'] + weights['Bond_Y']
    model.addConstraint(bond_allocation >= 0.2, name='MinBonds')  # At least 20% in bonds
    
    # Solve
    t0 = time.perf_counter()
    solution = model.solve()
    t1 = time.perf_counter()
    
    if solution:
        print("Optimal Portfolio Allocation:")
        total_return = 0
        total_risk = 0
        for asset in assets:
            weight = solution[f"w_{asset}"]
            asset_return = weight * expected_returns[asset]
            asset_risk = weight * risks[asset]
            total_return += asset_return
            total_risk += asset_risk
            print(f"  {asset:8}: {weight:6.1%} (return: {asset_return:5.1%}, risk: {asset_risk:5.1%})")
        
        print(f"\nPortfolio Summary:")
        print(f"  Expected Return: {total_return:5.1%}")
        print(f"  Risk Level: {total_risk:5.1%}")
        print(f"  Solve Time: {t1-t0:.4f}s")
    else:
        print("No feasible portfolio found!")
    
    return solution


def transportation_problem_example():
    """Solve a transportation problem using Gurddy."""
    print("\n=== Transportation Problem ===")
    
    # Supply and demand data
    suppliers = ['Factory_1', 'Factory_2', 'Factory_3']
    customers = ['Store_A', 'Store_B', 'Store_C', 'Store_D']
    
    supply = {'Factory_1': 100, 'Factory_2': 150, 'Factory_3': 120}
    demand = {'Store_A': 80, 'Store_B': 90, 'Store_C': 70, 'Store_D': 60}
    
    # Transportation costs (per unit)
    costs = {
        ('Factory_1', 'Store_A'): 4, ('Factory_1', 'Store_B'): 6, ('Factory_1', 'Store_C'): 8, ('Factory_1', 'Store_D'): 5,
        ('Factory_2', 'Store_A'): 3, ('Factory_2', 'Store_B'): 4, ('Factory_2', 'Store_C'): 6, ('Factory_2', 'Store_D'): 7,
        ('Factory_3', 'Store_A'): 5, ('Factory_3', 'Store_B'): 3, ('Factory_3', 'Store_C'): 4, ('Factory_3', 'Store_D'): 6,
    }
    
    print(f"Suppliers: {suppliers}")
    print(f"Supply: {supply}")
    print(f"Customers: {customers}")
    print(f"Demand: {demand}")
    print(f"Total supply: {sum(supply.values())}, Total demand: {sum(demand.values())}")
    print()
    
    # Check if problem is balanced
    total_supply = sum(supply.values())
    total_demand = sum(demand.values())
    
    if total_supply != total_demand:
        print(f"Warning: Unbalanced problem (supply: {total_supply}, demand: {total_demand})")
    
    # Build model
    model = gurddy.Model("Transportation", "LP")
    
    # Variables: shipment quantities
    shipments = {}
    for supplier in suppliers:
        for customer in customers:
            var_name = f"ship_{supplier}_to_{customer}"
            shipments[(supplier, customer)] = model.addVar(var_name, low_bound=0, cat='Continuous')
    
    # Objective: minimize total transportation cost
    total_cost = sum(shipments[(s, c)] * costs[(s, c)] for s in suppliers for c in customers)
    model.setObjective(total_cost, sense='Minimize')
    
    # Supply constraints
    for supplier in suppliers:
        supplier_shipments = sum(shipments[(supplier, customer)] for customer in customers)
        model.addConstraint(supplier_shipments <= supply[supplier], name=f'Supply_{supplier}')
    
    # Demand constraints
    for customer in customers:
        customer_shipments = sum(shipments[(supplier, customer)] for supplier in suppliers)
        model.addConstraint(customer_shipments >= demand[customer], name=f'Demand_{customer}')
    
    # Solve
    t0 = time.perf_counter()
    solution = model.solve()
    t1 = time.perf_counter()
    
    if solution:
        print("Optimal Transportation Plan:")
        total_cost_value = 0
        
        # Print shipment matrix
        print(f"{'':12}", end='')
        for customer in customers:
            print(f"{customer:>10}", end='')
        print(f"{'Supply':>10}")
        
        for supplier in suppliers:
            print(f"{supplier:12}", end='')
            supplier_total = 0
            for customer in customers:
                quantity = solution[f"ship_{supplier}_to_{customer}"]
                supplier_total += quantity
                cost = quantity * costs[(supplier, customer)]
                total_cost_value += cost
                if quantity > 0:
                    print(f"{quantity:>10.1f}", end='')
                else:
                    print(f"{'':>10}", end='')
            print(f"{supply[supplier]:>10}")
        
        # Print demand row
        print(f"{'Demand':12}", end='')
        for customer in customers:
            customer_total = sum(solution[f"ship_{supplier}_to_{customer}"] for supplier in suppliers)
            print(f"{customer_total:>10.1f}", end='')
        print()
        
        print(f"\nTotal Transportation Cost: ${total_cost_value:.2f}")
        print(f"Solve Time: {t1-t0:.4f}s")
    else:
        print("No feasible transportation plan found!")
    
    return solution


def constraint_relaxation_analysis():
    """Demonstrate constraint relaxation analysis."""
    print("\n=== Constraint Relaxation Analysis ===")
    
    # Simple production problem with tight constraints
    model = gurddy.Model("Production_Tight", "LP")
    
    # Variables
    x1 = model.addVar("Product_1", low_bound=0, cat='Continuous')
    x2 = model.addVar("Product_2", low_bound=0, cat='Continuous')
    
    # Objective: maximize profit
    profit = x1 * 30 + x2 * 40
    model.setObjective(profit, sense='Maximize')
    
    # Original tight constraints
    model.addConstraint(x1 * 2 + x2 * 3 <= 100, name='Resource_A')  # Tight constraint
    model.addConstraint(x1 * 4 + x2 * 2 <= 120, name='Resource_B')  # Less tight
    model.addConstraint(x1 <= 25, name='Demand_Limit_1')
    model.addConstraint(x2 <= 30, name='Demand_Limit_2')
    
    # Solve original problem
    print("Solving original problem...")
    t0 = time.perf_counter()
    solution_original = model.solve()
    t1 = time.perf_counter()
    
    profit_val = 0  # Initialize with default value
    
    if solution_original:
        x1_val = solution_original['Product_1']
        x2_val = solution_original['Product_2']
        profit_val = x1_val * 30 + x2_val * 40
        
        print(f"Original Solution:")
        print(f"  Product_1: {x1_val:.2f}")
        print(f"  Product_2: {x2_val:.2f}")
        print(f"  Profit: ${profit_val:.2f}")
        print(f"  Solve Time: {t1-t0:.4f}s")
        
        # Check constraint utilization
        resource_a_usage = x1_val * 2 + x2_val * 3
        resource_b_usage = x1_val * 4 + x2_val * 2
        
        print(f"\nConstraint Analysis:")
        print(f"  Resource A: {resource_a_usage:.2f}/100 ({resource_a_usage/100*100:.1f}% utilized)")
        print(f"  Resource B: {resource_b_usage:.2f}/120 ({resource_b_usage/120*100:.1f}% utilized)")
        print(f"  Demand Limit 1: {x1_val:.2f}/25 ({x1_val/25*100:.1f}% utilized)")
        print(f"  Demand Limit 2: {x2_val:.2f}/30 ({x2_val/30*100:.1f}% utilized)")
    else:
        print("No feasible solution found!")
    
    # Now relax the tightest constraint (Resource A) by 20%
    print(f"\nRelaxing Resource A constraint by 20%...")
    model_relaxed = gurddy.Model("Production_Relaxed", "LP")
    
    x1_r = model_relaxed.addVar("Product_1", low_bound=0, cat='Continuous')
    x2_r = model_relaxed.addVar("Product_2", low_bound=0, cat='Continuous')
    
    profit_r = x1_r * 30 + x2_r * 40
    model_relaxed.setObjective(profit_r, sense='Maximize')
    
    # Relaxed constraints
    model_relaxed.addConstraint(x1_r * 2 + x2_r * 3 <= 120, name='Resource_A_Relaxed')  # 100 -> 120
    model_relaxed.addConstraint(x1_r * 4 + x2_r * 2 <= 120, name='Resource_B')
    model_relaxed.addConstraint(x1_r <= 25, name='Demand_Limit_1')
    model_relaxed.addConstraint(x2_r <= 30, name='Demand_Limit_2')
    
    t0 = time.perf_counter()
    solution_relaxed = model_relaxed.solve()
    t1 = time.perf_counter()
    
    if solution_relaxed:
        x1_r_val = solution_relaxed['Product_1']
        x2_r_val = solution_relaxed['Product_2']
        profit_r_val = x1_r_val * 30 + x2_r_val * 40
        
        print(f"Relaxed Solution:")
        print(f"  Product_1: {x1_r_val:.2f}")
        print(f"  Product_2: {x2_r_val:.2f}")
        print(f"  Profit: ${profit_r_val:.2f}")
        print(f"  Solve Time: {t1-t0:.4f}s")
        
        # 只有在原始问题有解的情况下才计算改进
        if solution_original:  # This check ensures solution exists
            profit_improvement = profit_r_val - profit_val
            print(f"\nImprovement from relaxation:")
            print(f"  Profit increase: ${profit_improvement:.2f}")
            print(f"  Percentage improvement: {profit_improvement/profit_val*100:.1f}%")
            print(f"  Shadow price of Resource A (approx): ${profit_improvement/20:.2f} per unit")


def performance_comparison():
    """Compare performance of different problem formulations."""
    print("\n=== Performance Comparison ===")
    
    # Test different problem sizes
    problem_sizes = [10, 20, 50]
    
    for n in problem_sizes:
        print(f"\nTesting {n}×{n} assignment problem...")
        
        # Create assignment problem: assign n workers to n jobs
        model = gurddy.Model(f"Assignment_{n}x{n}", "LP")
        
        # Variables: x[i][j] = 1 if worker i assigned to job j
        x = {}
        for i in range(n):
            for j in range(n):
                x[(i, j)] = model.addVar(f"x_{i}_{j}", low_bound=0, up_bound=1, cat='Continuous')
        
        # Objective: minimize total cost (random costs for demo)
        import random
        random.seed(42)  # For reproducible results
        costs = {(i, j): random.randint(1, 100) for i in range(n) for j in range(n)}
        
        total_cost = sum(x[(i, j)] * costs[(i, j)] for i in range(n) for j in range(n))
        model.setObjective(total_cost, sense='Minimize')
        
        # Constraints: each worker assigned to exactly one job
        for i in range(n):
            model.addConstraint(sum(x[(i, j)] for j in range(n)) == 1, name=f'Worker_{i}')
        
        # Constraints: each job assigned to exactly one worker
        for j in range(n):
            model.addConstraint(sum(x[(i, j)] for i in range(n)) == 1, name=f'Job_{j}')
        
        # Solve and time
        t0 = time.perf_counter()
        solution = model.solve()
        t1 = time.perf_counter()
        
        if solution:
            # Calculate objective value
            obj_value = sum(solution[f"x_{i}_{j}"] * costs[(i, j)] for i in range(n) for j in range(n))
            print(f"  Size: {n}×{n}, Variables: {n*n}, Constraints: {2*n}")
            print(f"  Optimal cost: {obj_value:.2f}")
            print(f"  Solve time: {t1-t0:.4f}s")
        else:
            print(f"  Failed to solve {n}×{n} problem")


def main():
    """Run all advanced LP examples."""
    print("Advanced Linear Programming Examples with Gurddy")
    print("=" * 60)
    
    # Run examples
    portfolio_optimization_example()
    transportation_problem_example()
    constraint_relaxation_analysis()
    performance_comparison()
    
    print("\n" + "=" * 60)
    print("Advanced LP Examples Summary:")
    print("1. Portfolio Optimization - Multi-constraint investment problem")
    print("2. Transportation Problem - Classic operations research problem")
    print("3. Constraint Relaxation - Sensitivity analysis techniques")
    print("4. Performance Comparison - Scalability testing")
    print("\nThese examples demonstrate Gurddy's capability for:")
    print("- Complex multi-constraint optimization")
    print("- Real-world business problems")
    print("- Sensitivity and what-if analysis")
    print("- Performance benchmarking")


if __name__ == "__main__":
    main()