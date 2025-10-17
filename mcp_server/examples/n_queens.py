"""
N-Queens Problem using Gurddy CSP Solver

The N-Queens problem asks to place N queens on an N×N chessboard 
such that no two queens attack each other.
"""

import gurddy

def solve_n_queens(n=8):
    """Solve the N-Queens problem for an n×n board."""
    model = gurddy.Model(f"{n}-Queens", "CSP")
    
    # Variables: one for each row, value represents column position
    queens = {}
    for row in range(n):
        var_name = f"queen_row_{row}"
        queens[var_name] = model.addVar(var_name, domain=list(range(n)))
    
    # Constraint 1: All queens in different columns (AllDifferent)
    model.addConstraint(gurddy.AllDifferentConstraint(list(queens.values())))
    
    # Constraint 2: No two queens on same diagonal
    # For queens at (r1,c1) and (r2,c2): |r1-r2| != |c1-c2|
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
    return solution

def print_board(solution, n):
    """Print the chess board with queens."""
    if not solution:
        print("No solution found!")
        return
    
    print(f"\n{n}-Queens Solution:")
    print("+" + "---+" * n)
    
    for row in range(n):
        line = "|"
        queen_col = solution[f"queen_row_{row}"]
        for col in range(n):
            if col == queen_col:
                line += " Q |"
            else:
                line += "   |"
        print(line)
        print("+" + "---+" * n)
    
    # Print queen positions
    positions = []
    for row in range(n):
        col = solution[f"queen_row_{row}"]
        positions.append(f"({row},{col})")
    print(f"Queen positions: {', '.join(positions)}")

if __name__ == "__main__":
    # Solve 8-Queens
    print("Solving 8-Queens problem...")
    solution = solve_n_queens(8)
    print_board(solution, 8)
    
    # Try smaller boards
    for n in [4, 6]:
        print(f"\nSolving {n}-Queens problem...")
        solution = solve_n_queens(n)
        if solution:
            print_board(solution, n)
        else:
            print(f"No solution exists for {n}-Queens")