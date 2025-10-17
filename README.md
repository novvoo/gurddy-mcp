gurddy-mcp
=========

This repository contains a fully functional MCP (Model Context Protocol) server, providing solutions for Constraint Satisfaction Problems (CSP) and Linear Programming (LP). It is based on the `gurddy` package and supports solving a variety of classic problems.

## Main Features

### CSP Problem Solving
- **N-Queens Problem**: Place N queens on an N×N chessboard so that they do not attack each other
- **Graph Coloring Problem**: Assign colors to graph vertices so that adjacent vertices have different colors
- **Map Coloring Problem**: Assign colors to map regions so that adjacent regions have different colors
- **Sudoku Solving**: Solve 9×9 Sudoku puzzles
- **General CSP Solver**: Supports custom constraint satisfaction problems

### LP/Optimization Problems
- **Linear Programming**: Solve optimization problems with linear objective functions and constraints
- **Production Planning**: Solve production optimization problems under resource constraints
- **Integer Programming**: Supports optimization problems with integer variables

### HTTP API Service
- RESTful API interface, supporting JSON requests and responses
- Comprehensive error handling and performance monitoring
- Supports online solving of various CSP and LP problems

## Quick Start

### Environment Preparation
```bash
# Install dependencies
pip install -r requirements.txt

# Or manually install the main dependencies
pip install fastapi uvicorn gurddy pulp requests
```

## Usage

### 1. HTTP API Service

Start the HTTP server:
```bash
uvicorn mcp_server.http_api:app --host 127.0.0.1 --port 8000
```

Access the API documentation: http://127.0.0.1:8000/docs

### 2. Directly Calling the Demo

Run the complete CSP functionality demonstration:
```bash
python demo_csp_examples.py
```

Test the API functions (no server required):
```bash
python test_api_direct.py
```

### 3. Command Line Tools

Check/Install gurddy:
```bash
python -c "from mcp_server.tools.gurddy_install import run; print(run({'package':'gurddy'}))"
```

Run example:
```bash
python -c "from mcp_server.tools.gurddy_demo import run; print(run({'example':'csp'}))"
```

## API endpoint

### CSP problem solution

#### N-Queens problem
```bash
POST /solve-n-queens
{
"n": 8
}
```

#### Graph coloring problem
```bash
POST /solve-graph-coloring
{
"edges": [[0,1], [1,2], [2,0]],
"num_vertices": 3,
"max_colors": 3
}
```

#### Map coloring problem
```bash
POST /solve-map-coloring
{
"regions": ["A", "B", "C"],
"adjacencies": [["A", "B"], ["B", "C"]],
"max_colors": 2
}
```

#### Sudoku Solver
```bash
POST /solve-sudoku
{
"puzzle": [[5,3,0,...], [6,0,0,...], ...]
}
```

#### General CSP Solver
```bash
POST /solve-csp
{
"problem_type": "n_queens",
"parameters": {"n": 4}
}
```

### LP/Optimization Problems

#### Linear Programming
```bash
POST /solve-lp
{
"problem": {
"profits": {"ProductA": 10, "ProductB": 15},
"consumption": {
"ProductA": {"Resource1": 2, "Resource2": 1},
"ProductB": {"Resource1": 1, "Resource2": 3}
},
"capacities": {"Resource1": 100, "Resource2": 80}
}
}
```

#### Production Planning
```bash
POST /solve-production-planning
{
"profits": {"ProductA": 10, "ProductB": 15},
"consumption": {...},
"capacities": {...},
"integer": true,
"sensitivity_analysis": false
}
```

## Project Structure

```
mcp_server/
├── handlers/
│ └── gurddy.py # Core solver implementation
├── tools/ # MCP tool wrapper
├── examples/ # Rich CSP Problem Examples
│ ├── n_queens.py # N-Queens Problem
│ ├── graph_coloring.py # Graph Coloring Problem
│ ├── map_coloring.py # Map Coloring Problem
│ ├── logic_puzzles.py # Logic Puzzles
│ └── scheduling.py # Scheduling Problem
├── http_api.py # HTTP API Server
└── server.py # MCP Server

# Test and Demo Files
demo_csp_examples.py # Full Functionality Demonstration
test_api_direct.py # Direct API Test
test_csp_api.py # HTTP API Test
CSP_API_GUIDE.md # API Usage Guide

## Usage Examples

### Classic Problem Solving

#### Coloring the Australian Map
```python
import requests

response = requests.post("http://127.0.0.1:8000/solve-map-coloring", json={ 
"regions": ['WA', 'NT', 'SA', 'QLD', 'NSW', 'VIC', 'TAS'], 
"adjacencies": [ 
['WA', 'NT'], ['WA', 'SA'], ['NT', 'SA'], ['NT', 'QLD'], 
['SA', 'QLD'], ['SA', 'NSW'], ['SA', 'VIC'], 
['QLD', 'NSW'], ['NSW', 'VIC'] 
], 
"max_colors": 4
})
```

#### 8 Queen Problem
```python
response= requests.post("http://127.0.0.1:8000/solve-n-queens",
json={"n": 8})
```

#### Petersen Graph Coloring
```python
response = requests.post("http://127.0.0.1:8000/solve-graph-coloring", json={
"edges": [
[0,1], [1,2], [2,3], [3,4], [4,0], # Outer loop
[5,6], [6,7], [7,8], [8,9], [9,5], # Inner loop
[0,5], [1,6], [2,7], [3,8], [4,9] # Connections
],
"num_vertices": 10,
"max_colors": 3
})
```

## Supported Problem Types

### CSP Problems
- **N-Queens**: The classic N-Queens problem, supporting chessboards of any size
- **Graph Coloring**: Vertex coloring of arbitrary graph structures
- **Map Coloring**: Coloring geographic regions, verifying the Four Color Theorem
- **Sudoku**: Solving standard 9×9 Sudoku puzzles
- **Logic Puzzles**: Including classic logical reasoning problems such as the Zebra Puzzle
- **Scheduling**: Course scheduling, meeting scheduling, resource allocation, etc.

### Optimization Problems
- **Linear Programming**: Linear optimization with continuous variables
- **Integer Programming**: Optimization with discrete variables
- **Production Planning**: Production optimization under resource constraints
- **Mixed Integer Programming**: Optimization with a mix of continuous and discrete variables

## Performance Features

- **Fast Solution**: Typically completes in milliseconds for small to medium-sized problems (N-Queens with N ≤ 12, graph coloring with < 50 vertices)
- **Memory Efficient**: Uses backtracking search and constraint propagation, resulting in a small memory footprint.
- **Extensible**: Supports custom constraints and objective functions
- **Concurrency-Safe**: The HTTP API supports concurrent request processing

## Troubleshooting

### Common Errors
- `"gurddy package not available"`: Need to install the gurddy package
- `"No solution found"`: No solution found under the given constraints; try relaxing the constraints.
- `"Invalid input types"`: Check the data types of the input parameters.
- `"Unknown problem type"`: Use a supported problem type.

### Installation Issues
```bash
# If gurddy installation fails, try upgrading pip.

pip install --upgrade pip
pip install gurddy

# If PuLP installation fails,

pip install pulp

# Check the Python environment.

python -c "import sys; print(sys.executable)"

## Extension Development

### Adding a New CSP Problem
1. In `mcp_server/examples/` Create a problem implementation in `mcp_server/handlers/gurddy.py`
2. Add the solver function in `mcp_server/handlers/gurddy.py`
3. Add the API endpoint in `mcp_server/http_api.py`

### Custom Constraints
```python
# Define a custom constraint in gurddy
def custom_constraint(var1, var2):
return var1 + var2 <= 10

model.addConstraint(gurddy.FunctionConstraint(custom_constraint, (var1, var2)))
```

## License

This project is licensed under an open source license. Please see the LICENSE file for details.
