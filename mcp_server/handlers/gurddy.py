from __future__ import annotations

import os
import subprocess
import sys
from typing import Dict, Optional
from typing import List, Any

try:
    import gurddy
except Exception:  # pragma: no cover - gurddy may be external
    gurddy = None

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def pip_install(package: str, upgrade: bool = False) -> Dict[str, str]:
    """Install a Python package using pip in the current Python environment.

    Returns a dict with keys: success ("true"/"false"), output (str).
    """
    args = [sys.executable, '-m', 'pip', 'install']
    if upgrade:
        args.append('--upgrade')
    args.append(package)

    try:
        completed = subprocess.run(args, capture_output=True, text=True, check=False)
        success = completed.returncode == 0
        output = completed.stdout + '\n' + completed.stderr
    except Exception as e:
        return {"success": "false", "output": str(e)}

    return {"success": "true" if success else "false", "output": output}


def info() -> Dict[str, str]:
    """Return a short project description for gurddy (pulled from packaged description hardcoded here).

    This avoids network access and provides the MCP summary.
    """
    desc = (
        "Gurddy MCP Server provides comprehensive optimization and problem-solving capabilities through MCP. "
        "Supports CSP (N-Queens, Graph/Map Coloring, Sudoku, Logic Puzzles, Scheduling), "
        "LP/MIP (Linear Programming, Production Planning, Portfolio Optimization), "
        "and Game Theory (Minimax, Zero-Sum Games, Robust Optimization). "
        "Built on gurddy optimization library with PuLP integration. "
        "Available via stdio (IDE integration) and HTTP/SSE (web clients)."
    )
    return {"name": "gurddy", "description": desc}


def run_example(example_name: str) -> Dict[str, Optional[str]]:
    """Run one of the bundled example scripts (lp or csp).

    Returns a dict with keys: rc (int), output (str).
    """
    examples_dir = os.path.join(ROOT, 'examples')
    
    # Map example names to specific script files
    example_scripts = {
        'lp': 'optimized_lp.py',
        'csp': 'n_queens.py',
        'n_queens': 'n_queens.py',
        'graph_coloring': 'graph_coloring.py',
        'map_coloring': 'map_coloring.py',
        'scheduling': 'scheduling.py',
        'logic_puzzles': 'logic_puzzles.py',
        'optimized_csp': 'optimized_csp.py',
        'optimized_lp': 'optimized_lp.py',
        'minimax': 'minimax.py'
    }
    
    if example_name not in example_scripts:
        available = ', '.join(example_scripts.keys())
        return {"rc": 1, "output": f"Unknown example '{example_name}'. Available examples: {available}"}
    
    script = os.path.join(examples_dir, example_scripts[example_name])
    
    if not os.path.exists(script):
        return {"rc": 1, "output": f"Example script not found: {script}"}

    try:
        completed = subprocess.run([sys.executable, script], capture_output=True, text=True, check=False)
        output = completed.stdout
        if completed.stderr:
            output += '\n--- STDERR ---\n' + completed.stderr
        return {"rc": completed.returncode, "output": output}
    except Exception as e:
        return {"rc": 1, "output": f"Error running example: {str(e)}"}


def solve_sudoku(puzzle: List[List[int]]) -> Dict[str, Any]:
    """Solve a 9x9 Sudoku puzzle using the gurddy Model API.

    puzzle: list of 9 lists each with 9 ints (0 for empty)
    Returns dict: { 'success': bool, 'solution': [[ints]] or None, 'error': str or None }
    """
    if gurddy is None:
        return {"success": False, "solution": None, "error": "gurddy package not available"}

    # basic validation
    if not isinstance(puzzle, list) or len(puzzle) != 9:
        return {"success": False, "solution": None, "error": "puzzle must be 9x9 list"}

    for row in puzzle:
        if not isinstance(row, list) or len(row) != 9:
            return {"success": False, "solution": None, "error": "puzzle must be 9x9 list"}

    model = gurddy.Model(name="SudokuCSP", problem_type="CSP")
    vars_dict = {}
    for r in range(1, 10):
        for c in range(1, 10):
            var_name = f"cell_{r}_{c}"
            vars_dict[var_name] = model.addVar(var_name, domain=list(range(1, 10)))

    # Row constraints
    for r in range(1, 10):
        row_vars = [vars_dict[f"cell_{r}_{c}"] for c in range(1, 10)]
        model.addConstraint(gurddy.AllDifferentConstraint(row_vars))

    # Column constraints
    for c in range(1, 10):
        col_vars = [vars_dict[f"cell_{r}_{c}"] for r in range(1, 10)]
        model.addConstraint(gurddy.AllDifferentConstraint(col_vars))

    # 3x3 blocks
    for br in range(3):
        for bc in range(3):
            block_vars = []
            for i in range(3):
                for j in range(3):
                    row = br * 3 + i + 1
                    col = bc * 3 + j + 1
                    block_vars.append(vars_dict[f"cell_{row}_{col}"])
            model.addConstraint(gurddy.AllDifferentConstraint(block_vars))

    # Add givens
    for r in range(9):
        for c in range(9):
            val = puzzle[r][c]
            if isinstance(val, int) and val != 0:
                var = vars_dict[f"cell_{r+1}_{c+1}"]
                model.addConstraint(var == val)

    solution = model.solve()
    if not solution:
        return {"success": False, "solution": None, "error": "No solution found"}

    # build grid
    grid = []
    for r in range(1, 10):
        row_vals = [int(solution[f"cell_{r}_{c}"]) for c in range(1, 10)]
        grid.append(row_vals)

    return {"success": True, "solution": grid, "error": None}


def solve_lp(problem: Dict[str, Any]) -> Dict[str, Any]:
    """Solve a simple LP/MIP problem using PuLP.

    Expected problem dict keys:
      - profits: dict mapping product -> coefficient (objective)
      - consumption: dict mapping product -> dict(resource -> coefficient)
      - capacities: dict mapping resource -> capacity (RHS)
      - integer: optional bool (default True)

    Returns dict with keys: success (bool), status (str), objective (float), values (dict), time_seconds (float), error
    """
    try:
        import time
        import pulp
    except Exception as e:
        return {"success": False, "error": f"PuLP not available: {e}", "status": None}

    # basic validation and defaults
    profits = problem.get('profits')
    consumption = problem.get('consumption')
    capacities = problem.get('capacities')
    integer = bool(problem.get('integer', True))

    if not (isinstance(profits, dict) and isinstance(consumption, dict) and isinstance(capacities, dict)):
        return {"success": False, "error": "invalid problem format: profits/consumption/capacities required", "status": None}

    try:
        t0 = time.perf_counter()
        products = list(profits.keys())
        prob = pulp.LpProblem('mcp_lp', pulp.LpMaximize)
        qty = {}
        for p in products:
            if integer:
                qty[p] = pulp.LpVariable(f'q_{p}', lowBound=0, cat=pulp.LpInteger)
            else:
                qty[p] = pulp.LpVariable(f'q_{p}', lowBound=0, cat=pulp.LpContinuous)

        # objective
        prob += pulp.lpSum([profits[p] * qty[p] for p in products])

        # resource constraints
        for r, cap in capacities.items():
            prob += (pulp.lpSum([consumption[p].get(r, 0) * qty[p] for p in products]) <= cap), f'Res_{r}'

        solver_cmd = pulp.PULP_CBC_CMD(msg=False)
        status = prob.solve(solver_cmd)
        t1 = time.perf_counter()
        obj = pulp.value(prob.objective)
        vals = {p: float(qty[p].varValue) for p in products}
        return {"success": True, "status": pulp.LpStatus[status], "objective": obj, "values": vals, "time_seconds": t1 - t0, "error": None}
    except Exception as e:
        return {"success": False, "error": str(e), "status": None}


def solve_n_queens(n: int = 8) -> Dict[str, Any]:
    """Solve the N-Queens problem for an n×n board."""
    if gurddy is None:
        return {"success": False, "solution": None, "error": "gurddy package not available"}
    
    if not isinstance(n, int) or n < 1:
        return {"success": False, "solution": None, "error": "n must be a positive integer"}
    
    try:
        model = gurddy.Model(f"{n}-Queens", "CSP")
        
        # Variables: one for each row, value represents column position
        queens = {}
        for row in range(n):
            var_name = f"queen_row_{row}"
            queens[var_name] = model.addVar(var_name, domain=list(range(n)))
        
        # Constraint 1: All queens in different columns (AllDifferent)
        model.addConstraint(gurddy.AllDifferentConstraint(list(queens.values())))
        
        # Constraint 2: No two queens on same diagonal
        queen_vars = list(queens.values())
        for i in range(n):
            for j in range(i + 1, n):
                row_diff = j - i
                # Create constraint function with fixed row difference
                def make_diagonal_constraint(rd):
                    def not_on_same_diagonal(col1, col2):
                        return abs(col1 - col2) != rd
                    return not_on_same_diagonal
                
                constraint_func = make_diagonal_constraint(row_diff)
                model.addConstraint(gurddy.FunctionConstraint(constraint_func, (queen_vars[i], queen_vars[j])))
        
        # Solve
        solution = model.solve()
        if not solution:
            return {"success": False, "solution": None, "error": "No solution found"}
        
        # Format solution as list of column positions
        positions = []
        for row in range(n):
            col = solution[f"queen_row_{row}"]
            positions.append(col)
        
        return {"success": True, "solution": positions, "error": None}
    except Exception as e:
        return {"success": False, "solution": None, "error": str(e)}


def solve_graph_coloring(edges: List[List[int]], num_vertices: int, max_colors: int = 4) -> Dict[str, Any]:
    """Solve graph coloring problem."""
    if gurddy is None:
        return {"success": False, "solution": None, "error": "gurddy package not available"}
    
    if not isinstance(edges, list) or not isinstance(num_vertices, int) or not isinstance(max_colors, int):
        return {"success": False, "solution": None, "error": "Invalid input types"}
    
    if num_vertices < 1 or max_colors < 1:
        return {"success": False, "solution": None, "error": "num_vertices and max_colors must be positive"}
    
    try:
        model = gurddy.Model("GraphColoring", "CSP")
        
        # Variables: one for each vertex, domain is available colors
        vertices = {}
        for v in range(num_vertices):
            var_name = f"vertex_{v}"
            vertices[var_name] = model.addVar(var_name, domain=list(range(max_colors)))
        
        # Constraints: Adjacent vertices must have different colors
        def different_colors(color1, color2):
            return color1 != color2
        
        for edge in edges:
            if len(edge) != 2:
                return {"success": False, "solution": None, "error": "Each edge must have exactly 2 vertices"}
            v1, v2 = edge
            if v1 >= num_vertices or v2 >= num_vertices or v1 < 0 or v2 < 0:
                return {"success": False, "solution": None, "error": f"Vertex indices must be between 0 and {num_vertices-1}"}
            
            var1 = vertices[f"vertex_{v1}"]
            var2 = vertices[f"vertex_{v2}"]
            model.addConstraint(gurddy.FunctionConstraint(different_colors, (var1, var2)))
        
        # Solve
        solution = model.solve()
        if not solution:
            return {"success": False, "solution": None, "error": "No solution found"}
        
        # Format solution as list of colors for each vertex
        colors = []
        for v in range(num_vertices):
            color = solution[f"vertex_{v}"]
            colors.append(color)
        
        return {"success": True, "solution": colors, "error": None}
    except Exception as e:
        return {"success": False, "solution": None, "error": str(e)}


def solve_map_coloring(regions: List[str], adjacencies: List[List[str]], max_colors: int = 4) -> Dict[str, Any]:
    """Solve map coloring problem."""
    if gurddy is None:
        return {"success": False, "solution": None, "error": "gurddy package not available"}
    
    if not isinstance(regions, list) or not isinstance(adjacencies, list) or not isinstance(max_colors, int):
        return {"success": False, "solution": None, "error": "Invalid input types"}
    
    if len(regions) < 1 or max_colors < 1:
        return {"success": False, "solution": None, "error": "regions and max_colors must be positive"}
    
    try:
        model = gurddy.Model("MapColoring", "CSP")
        
        # Variables: one for each region
        region_vars = {}
        for region in regions:
            region_vars[region] = model.addVar(region, domain=list(range(max_colors)))
        
        # Constraints: Adjacent regions must have different colors
        def different_colors(color1, color2):
            return color1 != color2
        
        for adjacency in adjacencies:
            if len(adjacency) != 2:
                return {"success": False, "solution": None, "error": "Each adjacency must have exactly 2 regions"}
            region1, region2 = adjacency
            if region1 not in regions or region2 not in regions:
                return {"success": False, "solution": None, "error": f"Unknown region in adjacency: {region1}, {region2}"}
            
            var1 = region_vars[region1]
            var2 = region_vars[region2]
            model.addConstraint(gurddy.FunctionConstraint(different_colors, (var1, var2)))
        
        # Solve
        solution = model.solve()
        if not solution:
            return {"success": False, "solution": None, "error": "No solution found"}
        
        # Format solution as dict mapping region to color
        result = {}
        for region in regions:
            color = solution[region]
            result[region] = color
        
        return {"success": True, "solution": result, "error": None}
    except Exception as e:
        return {"success": False, "solution": None, "error": str(e)}


def solve_csp_generic(problem_type: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Generic CSP solver dispatcher."""
    if problem_type == "n_queens":
        n = parameters.get("n", 8)
        return solve_n_queens(n)
    elif problem_type == "graph_coloring":
        edges = parameters.get("edges", [])
        num_vertices = parameters.get("num_vertices", 0)
        max_colors = parameters.get("max_colors", 4)
        return solve_graph_coloring(edges, num_vertices, max_colors)
    elif problem_type == "map_coloring":
        regions = parameters.get("regions", [])
        adjacencies = parameters.get("adjacencies", [])
        max_colors = parameters.get("max_colors", 4)
        return solve_map_coloring(regions, adjacencies, max_colors)
    else:
        return {"success": False, "solution": None, "error": f"Unknown problem type: {problem_type}"}


def solve_production_planning(profits: Dict[str, float], consumption: Dict[str, Dict[str, float]], 
                            capacities: Dict[str, float], integer: bool = True, 
                            sensitivity_analysis: bool = False) -> Dict[str, Any]:
    """Solve production planning problem (wrapper around solve_lp with additional features)."""
    problem = {
        "profits": profits,
        "consumption": consumption, 
        "capacities": capacities,
        "integer": integer
    }
    
    result = solve_lp(problem)
    
    if sensitivity_analysis and result.get("success"):
        # Add basic sensitivity analysis
        result["sensitivity"] = {
            "note": "Sensitivity analysis would show how changes in profits/capacities affect the solution",
            "implemented": False
        }
    
    return result


def solve_minimax_game(payoff_matrix: List[List[float]], player: str = "row") -> Dict[str, Any]:
    """Solve a two-player zero-sum game using minimax.
    
    Args:
        payoff_matrix: 2D list representing payoffs (row player's perspective)
        player: "row" for maximizer or "col" for minimizer
        
    Returns:
        Dict with success, strategy (list of probabilities), value (game value), and error
    """
    if gurddy is None:
        return {"success": False, "strategy": None, "value": None, "error": "gurddy package not available"}
    
    if not isinstance(payoff_matrix, list) or len(payoff_matrix) == 0:
        return {"success": False, "strategy": None, "value": None, "error": "payoff_matrix must be a non-empty 2D list"}
    
    if not isinstance(player, str) or player not in ["row", "col"]:
        return {"success": False, "strategy": None, "value": None, "error": "player must be 'row' or 'col'"}
    
    try:
        from gurddy.solver.minimax_solver import MinimaxSolver
        
        solver = MinimaxSolver(None)
        result = solver.solve_game_matrix(payoff_matrix, player=player)
        
        return {
            "success": True,
            "strategy": result["strategy"],
            "value": result["value"],
            "error": None
        }
    except Exception as e:
        return {"success": False, "strategy": None, "value": None, "error": str(e)}


def solve_minimax_decision(scenarios: List[Dict[str, float]], decision_vars: List[str], 
                          budget: float = 100.0, objective: str = "minimize_max_loss") -> Dict[str, Any]:
    """Solve a minimax decision problem under uncertainty.
    
    Args:
        scenarios: List of dicts mapping decision variables to coefficients (loss/gain)
        decision_vars: List of decision variable names
        budget: Total budget constraint
        objective: "minimize_max_loss" or "maximize_min_gain"
        
    Returns:
        Dict with success, decision (dict of allocations), objective_value, and error
    """
    if gurddy is None:
        return {"success": False, "decision": None, "objective_value": None, "error": "gurddy package not available"}
    
    if not isinstance(scenarios, list) or len(scenarios) == 0:
        return {"success": False, "decision": None, "objective_value": None, "error": "scenarios must be a non-empty list"}
    
    if not isinstance(decision_vars, list) or len(decision_vars) == 0:
        return {"success": False, "decision": None, "objective_value": None, "error": "decision_vars must be a non-empty list"}
    
    try:
        from gurddy.solver.minimax_solver import MinimaxSolver
        
        solver = MinimaxSolver(None)
        
        if objective == "minimize_max_loss":
            result = solver.solve_minimax_decision(scenarios, decision_vars, budget=budget)
            return {
                "success": True,
                "decision": result["decision"],
                "objective_value": result["max_loss"],
                "objective_type": "max_loss",
                "error": None
            }
        elif objective == "maximize_min_gain":
            result = solver.solve_maximin_decision(scenarios, decision_vars, budget=budget)
            return {
                "success": True,
                "decision": result["decision"],
                "objective_value": result["min_gain"],
                "objective_type": "min_gain",
                "error": None
            }
        else:
            return {"success": False, "decision": None, "objective_value": None, 
                   "error": f"Unknown objective: {objective}. Use 'minimize_max_loss' or 'maximize_min_gain'"}
    except Exception as e:
        return {"success": False, "decision": None, "objective_value": None, "error": str(e)}

