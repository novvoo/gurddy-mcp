"""
Minimax Problem Examples using Gurddy

This module demonstrates various minimax optimization problems:
1. Zero-sum game theory (Rock-Paper-Scissors, Matching Pennies)
2. Portfolio optimization (minimize maximum loss)
3. Robust optimization (worst-case scenario planning)
4. Competitive facility location
5. Security games (attacker-defender scenarios)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from gurddy.solver.minimax_solver import MinimaxSolver


def print_section(title):
    """Print formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def example_rock_paper_scissors():
    """
    Classic Rock-Paper-Scissors game.
    Payoff matrix (row player perspective):
    - Rock beats Scissors (+1), loses to Paper (-1), ties with Rock (0)
    """
    print_section("Example 1: Rock-Paper-Scissors Game")
    
    # Payoff matrix: rows = [Rock, Paper, Scissors], cols = [Rock, Paper, Scissors]
    payoff_matrix = [
        [0, -1, 1],   # Rock vs [Rock, Paper, Scissors]
        [1, 0, -1],   # Paper vs [Rock, Paper, Scissors]
        [-1, 1, 0]    # Scissors vs [Rock, Paper, Scissors]
    ]
    
    solver = MinimaxSolver(None)
    
    # Solve for row player (maximizer)
    result_row = solver.solve_game_matrix(payoff_matrix, player="row")
    print("\nRow Player (Maximizer) Strategy:")
    print(f"  Rock:     {result_row['strategy'][0]:.4f}")
    print(f"  Paper:    {result_row['strategy'][1]:.4f}")
    print(f"  Scissors: {result_row['strategy'][2]:.4f}")
    print(f"  Game Value: {result_row['value']:.4f}")
    
    # Solve for column player (minimizer)
    result_col = solver.solve_game_matrix(payoff_matrix, player="col")
    print("\nColumn Player (Minimizer) Strategy:")
    print(f"  Rock:     {result_col['strategy'][0]:.4f}")
    print(f"  Paper:    {result_col['strategy'][1]:.4f}")
    print(f"  Scissors: {result_col['strategy'][2]:.4f}")
    print(f"  Game Value: {result_col['value']:.4f}")
    
    print("\n✓ Optimal strategy: Play each move with equal probability (1/3)")
    print("✓ Game value is 0 (fair game)")


def example_matching_pennies():
    """
    Matching Pennies: Two players simultaneously choose Heads or Tails.
    If they match, Player 1 wins. If they don't match, Player 2 wins.
    """
    print_section("Example 2: Matching Pennies Game")
    
    # Payoff matrix: rows = [Heads, Tails], cols = [Heads, Tails]
    payoff_matrix = [
        [1, -1],   # Player 1 Heads vs [Heads, Tails]
        [-1, 1]    # Player 1 Tails vs [Heads, Tails]
    ]
    
    solver = MinimaxSolver(None)
    
    result_row = solver.solve_game_matrix(payoff_matrix, player="row")
    print("\nPlayer 1 (Matcher) Strategy:")
    print(f"  Heads: {result_row['strategy'][0]:.4f}")
    print(f"  Tails: {result_row['strategy'][1]:.4f}")
    print(f"  Expected Payoff: {result_row['value']:.4f}")
    
    result_col = solver.solve_game_matrix(payoff_matrix, player="col")
    print("\nPlayer 2 (Mismatcher) Strategy:")
    print(f"  Heads: {result_col['strategy'][0]:.4f}")
    print(f"  Tails: {result_col['strategy'][1]:.4f}")
    print(f"  Expected Payoff: {result_col['value']:.4f}")
    
    print("\n✓ Both players should randomize 50-50")
    print("✓ Game value is 0 (fair game)")


def example_portfolio_optimization():
    """
    Portfolio optimization: Minimize maximum loss across different market scenarios.
    Investor allocates budget across 3 assets.
    """
    print_section("Example 3: Robust Portfolio Optimization")
    
    print("\nProblem: Allocate $100 across 3 assets to minimize worst-case loss")
    print("Assets: Stock A, Stock B, Bond C")
    print("\nScenarios (loss per dollar invested):")
    print("  Bull Market:  A=-0.2, B=-0.1, C=0.05  (stocks gain, bonds lose)")
    print("  Bear Market:  A=0.3,  B=0.2,  C=-0.02 (stocks lose, bonds gain)")
    print("  Stable:       A=0.05, B=0.03, C=-0.01 (small movements)")
    
    # Scenarios: loss coefficients for each asset
    scenarios = [
        {"A": -0.2, "B": -0.1, "C": 0.05},   # Bull market (negative = gain)
        {"A": 0.3, "B": 0.2, "C": -0.02},    # Bear market
        {"A": 0.05, "B": 0.03, "C": -0.01}   # Stable market
    ]
    
    solver = MinimaxSolver(None)
    result = solver.solve_minimax_decision(scenarios, ["A", "B", "C"], budget=100)
    
    print("\nOptimal Allocation (minimize maximum loss):")
    print(f"  Stock A: ${result['decision']['A']:.2f}")
    print(f"  Stock B: ${result['decision']['B']:.2f}")
    print(f"  Bond C:  ${result['decision']['C']:.2f}")
    print(f"  Total:   ${sum(result['decision'].values()):.2f}")
    print(f"\nWorst-case loss: ${result['max_loss']:.2f}")
    
    # Calculate loss in each scenario
    print("\nLoss in each scenario:")
    for i, scenario in enumerate(scenarios):
        loss = sum(scenario[asset] * result['decision'][asset] for asset in ["A", "B", "C"])
        scenario_names = ["Bull Market", "Bear Market", "Stable Market"]
        print(f"  {scenario_names[i]}: ${loss:.2f}")
    
    print("\n✓ Minimax strategy balances risk across all scenarios")


def example_production_planning():
    """
    Production planning: Maximize minimum profit across uncertain demand scenarios.
    """
    print_section("Example 4: Robust Production Planning")
    
    print("\nProblem: Produce 2 products to maximize worst-case profit")
    print("Products: Widget X, Gadget Y")
    print("\nDemand Scenarios (profit per unit):")
    print("  High Demand:   X=$50, Y=$40")
    print("  Medium Demand: X=$30, Y=$35")
    print("  Low Demand:    X=$20, Y=$25")
    
    # Scenarios: profit coefficients (negative because we're maximizing)
    scenarios = [
        {"X": -50, "Y": -40},   # High demand (negative for maximin)
        {"X": -30, "Y": -35},   # Medium demand
        {"X": -20, "Y": -25}    # Low demand
    ]
    
    solver = MinimaxSolver(None)
    result = solver.solve_maximin_decision(scenarios, ["X", "Y"], budget=100)
    
    print("\nOptimal Production (maximize minimum profit):")
    print(f"  Widget X: {result['decision']['X']:.2f} units")
    print(f"  Gadget Y: {result['decision']['Y']:.2f} units")
    
    # Calculate actual profits (negate because scenarios use negative values)
    profits = []
    for scenario in scenarios:
        profit = -sum(scenario[product] * result['decision'][product] for product in ["X", "Y"])
        profits.append(profit)
    
    min_profit = min(profits)
    print(f"\nGuaranteed minimum profit: ${min_profit:.2f}")
    
    # Calculate profit in each scenario
    print("\nProfit in each scenario:")
    scenario_names = ["High Demand", "Medium Demand", "Low Demand"]
    for i, profit in enumerate(profits):
        print(f"  {scenario_names[i]}: ${profit:.2f}")
    
    print("\n✓ Maximin strategy ensures minimum profit guarantee")


def example_battle_of_sexes():
    """
    Battle of the Sexes: Coordination game with conflicting preferences.
    Couple wants to spend evening together but prefer different activities.
    """
    print_section("Example 5: Battle of the Sexes Game")
    
    print("\nScenario: Couple choosing between Opera and Football")
    print("Both prefer being together over being apart")
    print("But have different preferences for activities")
    
    # Payoff matrix (Player 1's payoff): rows = [Opera, Football], cols = [Opera, Football]
    payoff_matrix = [
        [2, 0],    # Player 1 chooses Opera: (both Opera=2, split=0)
        [0, 1]     # Player 1 chooses Football: (split=0, both Football=1)
    ]
    
    solver = MinimaxSolver(None)
    
    result_row = solver.solve_game_matrix(payoff_matrix, player="row")
    print("\nPlayer 1 (prefers Opera) Mixed Strategy:")
    print(f"  Opera:    {result_row['strategy'][0]:.4f}")
    print(f"  Football: {result_row['strategy'][1]:.4f}")
    print(f"  Expected Payoff: {result_row['value']:.4f}")
    
    result_col = solver.solve_game_matrix(payoff_matrix, player="col")
    print("\nPlayer 2 (prefers Football) Mixed Strategy:")
    print(f"  Opera:    {result_col['strategy'][0]:.4f}")
    print(f"  Football: {result_col['strategy'][1]:.4f}")
    print(f"  Expected Payoff: {result_col['value']:.4f}")
    
    print("\n✓ Mixed strategy equilibrium exists but pure coordination is better")
    print("✓ This game has multiple Nash equilibria")


def example_security_game():
    """
    Security game: Defender allocates resources, attacker chooses target.
    """
    print_section("Example 6: Security Resource Allocation")
    
    print("\nScenario: Protect 3 targets from attack")
    print("Defender has limited resources, attacker chooses one target")
    print("\nPayoff matrix (defender's loss if target attacked):")
    print("  Target 1 (High Value):   Unprotected=-10, Protected=-2")
    print("  Target 2 (Medium Value): Unprotected=-6,  Protected=-1")
    print("  Target 3 (Low Value):    Unprotected=-3,  Protected=-0.5")
    
    # Simplified: Defender chooses protection level, Attacker chooses target
    # Payoff = defender's loss (negative values)
    # Rows = defender strategies, Cols = attacker targets
    payoff_matrix = [
        [-10, -6, -3],      # No protection
        [-2, -6, -3],       # Protect Target 1
        [-10, -1, -3],      # Protect Target 2
        [-10, -6, -0.5],    # Protect Target 3
        [-2, -1, -3],       # Protect Targets 1&2
        [-2, -6, -0.5],     # Protect Targets 1&3
        [-10, -1, -0.5]     # Protect Targets 2&3
    ]
    
    solver = MinimaxSolver(None)
    
    result_row = solver.solve_game_matrix(payoff_matrix, player="row")
    print("\nDefender's Optimal Mixed Strategy:")
    strategies = ["None", "T1", "T2", "T3", "T1&T2", "T1&T3", "T2&T3"]
    for i, prob in enumerate(result_row['strategy']):
        if prob > 0.01:  # Only show strategies with significant probability
            print(f"  Protect {strategies[i]}: {prob:.4f}")
    print(f"\nExpected Loss: {result_row['value']:.2f}")
    
    result_col = solver.solve_game_matrix(payoff_matrix, player="col")
    print("\nAttacker's Optimal Mixed Strategy:")
    targets = ["Target 1 (High)", "Target 2 (Med)", "Target 3 (Low)"]
    for i, prob in enumerate(result_col['strategy']):
        if prob > 0.01:
            print(f"  Attack {targets[i]}: {prob:.4f}")
    print(f"\nExpected Loss: {result_col['value']:.2f}")
    
    print("\n✓ Defender randomizes to make attacker indifferent")
    print("✓ Attacker targets based on protection probability")


def example_advertising_competition():
    """
    Advertising competition: Two companies compete for market share.
    """
    print_section("Example 7: Advertising Budget Competition")
    
    print("\nScenario: Two companies allocate advertising budget")
    print("Market share depends on relative spending")
    print("\nPayoff matrix (Company A's market share gain):")
    print("  Rows: Company A strategies [Low, Medium, High]")
    print("  Cols: Company B strategies [Low, Medium, High]")
    
    # Payoff matrix: Company A's market share change
    payoff_matrix = [
        [0, -5, -10],    # A: Low budget
        [5, 0, -3],      # A: Medium budget
        [10, 3, 0]       # A: High budget
    ]
    
    solver = MinimaxSolver(None)
    
    result_row = solver.solve_game_matrix(payoff_matrix, player="row")
    print("\nCompany A's Optimal Strategy:")
    budgets = ["Low Budget", "Medium Budget", "High Budget"]
    for i, prob in enumerate(result_row['strategy']):
        print(f"  {budgets[i]}: {prob:.4f}")
    print(f"  Expected Market Share Gain: {result_row['value']:.2f}%")
    
    result_col = solver.solve_game_matrix(payoff_matrix, player="col")
    print("\nCompany B's Optimal Strategy:")
    for i, prob in enumerate(result_col['strategy']):
        print(f"  {budgets[i]}: {prob:.4f}")
    print(f"  Expected Market Share Loss: {result_col['value']:.2f}%")
    
    print("\n✓ Companies balance budget allocation to maximize/minimize market share")


def main():
    """Run all minimax examples"""
    print("\n" + "=" * 70)
    print("  GURDDY MINIMAX SOLVER - COMPREHENSIVE EXAMPLES")
    print("=" * 70)
    print("\nMinimax optimization finds optimal strategies in adversarial")
    print("and uncertain environments by minimizing worst-case outcomes.")
    
    # Game theory examples
    example_rock_paper_scissors()
    example_matching_pennies()
    example_battle_of_sexes()
    
    # Decision theory examples
    example_portfolio_optimization()
    example_production_planning()
    
    # Applied examples
    example_security_game()
    example_advertising_competition()
    
    print("\n" + "=" * 70)
    print("  ALL MINIMAX EXAMPLES COMPLETED")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("  • Minimax finds optimal strategies in competitive scenarios")
    print("  • Mixed strategies often outperform pure strategies")
    print("  • Robust optimization handles uncertainty effectively")
    print("  • Game theory provides insights for strategic decision-making")
    print("\n")


if __name__ == "__main__":
    main()