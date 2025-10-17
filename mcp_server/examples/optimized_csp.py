import gurddy

# Example usage for CSP: Solving a Sudoku puzzle

# Create a CSP model
model = gurddy.Model(name="SudokuCSP", problem_type="CSP")

# Define variables: 81 variables for a 9x9 Sudoku grid, each with domain 1-9
vars_dict = {}
for row in range(1, 10):
    for col in range(1, 10):
        var_name = f"cell_{row}_{col}"
        vars_dict[var_name] = model.addVar(var_name, domain=[1, 2, 3, 4, 5, 6, 7, 8, 9])

# Add AllDifferent constraints for rows
for row in range(1, 10):
    row_vars = [vars_dict[f"cell_{row}_{col}"] for col in range(1, 10)]
    model.addConstraint(gurddy.AllDifferentConstraint(row_vars))

# Add AllDifferent constraints for columns
for col in range(1, 10):
    col_vars = [vars_dict[f"cell_{row}_{col}"] for row in range(1, 10)]
    model.addConstraint(gurddy.AllDifferentConstraint(col_vars))

# Add AllDifferent constraints for 3x3 subgrids
for block_row in range(3):
    for block_col in range(3):
        block_vars = []
        for i in range(3):
            for j in range(3):
                row = block_row * 3 + i + 1
                col = block_col * 3 + j + 1
                block_vars.append(vars_dict[f"cell_{row}_{col}"])
        model.addConstraint(gurddy.AllDifferentConstraint(block_vars))

# Example puzzle (0 means empty)
puzzle = [
        [0, 0, 0, 0, 0, 0, 0, 0, 3],
        [0, 0, 0, 0, 6, 3, 0, 4, 0],
        [0, 0, 4, 0, 0, 2, 6, 9, 7],
        [0, 9, 0, 7, 0, 0, 3, 1, 0],
        [3, 0, 0, 0, 0, 0, 0, 6, 4],
        [8, 0, 0, 0, 5, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 8, 2, 0, 0],
        [0, 7, 8, 0, 0, 0, 0, 0, 0],
        [4, 0, 2, 0, 0, 0, 0, 0, 0]
]

# Add equality constraints for given values in the puzzle
for row in range(9):
    for col in range(9):
        if puzzle[row][col] != 0:
            var = vars_dict[f"cell_{row+1}_{col+1}"]
            # Add constraint: var == value
            model.addConstraint(var == puzzle[row][col])

# Solve the CSP
solution = model.solve()

# Print the solution if found
if solution:
    print("Sudoku Solution:")
    for row in range(1, 10):
        row_values = [solution[f"cell_{row}_{col}"] for col in range(1, 10)]
        print(' '.join(map(str, row_values)))
else:
    print("No solution found.")