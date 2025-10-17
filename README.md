# Gurddy MCP Server

[![PyPI version](https://badge.fury.io/py/gurddy-mcp.svg)](https://pypi.org/project/gurddy_mcp/)
[![Python Support](https://img.shields.io/pypi/pyversions/gurddy_mcp.svg)](https://pypi.org/project/gurddy_mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-gurddy--mcp.fly.dev-blue)](https://gurddy-mcp.fly.dev)

A fully functional MCP (Model Context Protocol) server providing solutions for Constraint Satisfaction Problems (CSP) and Linear Programming (LP). Built on the `gurddy` optimization library, it supports solving a variety of classic problems through multiple interfaces.

**🚀 Quick Start:** `pip install gurddy_mcp && gurddy-mcp run-example n_queens`

**🌐 Live Demo:** [https://gurddy-mcp.fly.dev](https://gurddy-mcp.fly.dev)

**📦 PyPI Package:** [https://pypi.org/project/gurddy_mcp](https://pypi.org/project/gurddy_mcp)

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

## Installation

### From PyPI (Recommended)
```bash
# Install the latest stable version
pip install gurddy_mcp

# Or install with development dependencies
pip install gurddy_mcp[dev]
```

### From Source
```bash
# Clone the repository
git clone https://github.com/novvoo/gurddy-mcp.git
cd gurddy-mcp

# Install in development mode
pip install -e .

# Or install dependencies manually
pip install -r requirements.txt
```

### Verify Installation
```bash
# Check if installation was successful
gurddy-mcp info

# Run a quick example
gurddy-mcp run-example n_queens
```

## Usage

### 1. Command Line Interface

Run examples directly:
```bash
# Using the installed command (after pip install gurddy_mcp)
gurddy-mcp run-example n_queens
gurddy-mcp run-example graph_coloring
gurddy-mcp run-example map_coloring
gurddy-mcp run-example scheduling
gurddy-mcp run-example logic_puzzles
gurddy-mcp run-example optimized_csp
gurddy-mcp run-example lp
gurddy-mcp run-example optimized_lp

# Get package information
gurddy-mcp info

# Install or upgrade gurddy
gurddy-mcp install [--upgrade]

# Alternative: using Python module (from source)
python -m mcp_server.server run-example n_queens
python -m mcp_server.server info
```

### 2. HTTP API Service

Start the HTTP server:
```bash
# After installing gurddy_mcp
uvicorn mcp_server.http_api:app --host 127.0.0.1 --port 8080

# Or use the live demo
# https://gurddy-mcp.fly.dev
```

Access the API documentation: http://127.0.0.1:8080/docs

### 3. MCP (Model Context Protocol) Integration

Configure in `.kiro/settings/mcp.json`:
```json
{
  "mcpServers": {
    "gurddy-mcp": {
      "command": "gurddy-mcp",
      "disabled": false,
      "autoApprove": ["run_example", "info", "install"]
    }
  }
}
```

Alternative configuration (from source):
```json
{
  "mcpServers": {
    "gurddy-mcp": {
      "command": "python",
      "args": ["-m", "mcp_server.server"],
      "cwd": "/path/to/gurddy-mcp",
      "env": {
        "PYTHONPATH": "."
      },
      "disabled": false,
      "autoApprove": ["run_example", "info", "install"]
    }
  }
}
```

## Integration in Other Projects

### HTTP API Client
```python
import requests

# Use the deployed service
BASE_URL = "https://gurddy-mcp.fly.dev"

# Run examples
response = requests.post(f"{BASE_URL}/run-example", json={"example": "n_queens"})
print(response.json())

# Solve specific problems
response = requests.post(f"{BASE_URL}/solve-n-queens", json={"n": 8})
result = response.json()
if result["success"]:
    print(f"8-Queens solution: {result['solution']}")
```

### Direct Module Import
```python
# Install from PyPI
pip install gurddy_mcp

# Use in your project
from mcp_server import solve_n_queens, solve_graph_coloring

result = solve_n_queens(8)
if result['success']:
    print(f"Solution: {result['solution']}")

# Or import from specific modules
from mcp_server.handlers.gurddy import solve_n_queens, solve_sudoku
```

### Docker Integration
```dockerfile
# Dockerfile
FROM python:3.11-slim
RUN pip install gurddy_mcp
EXPOSE 8080
CMD ["uvicorn", "mcp_server.http_api:app", "--host", "0.0.0.0", "--port", "8080"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  gurddy-mcp:
    image: python:3.11-slim
    command: >
      sh -c "pip install gurddy_mcp && 
             uvicorn mcp_server.http_api:app --host 0.0.0.0 --port 8080"
    ports:
      - "8080:8080"
  your-app:
    build: .
    environment:
      - GURDDY_API_URL=http://gurddy-mcp:8080
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

## Example Output

### N-Queens Problem
```bash
$ python -m mcp_server.server run-example n_queens

Solving 8-Queens problem...

8-Queens Solution:
+---+---+---+---+---+---+---+---+
| Q |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   | Q |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   | Q |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   | Q |   |   |
+---+---+---+---+---+---+---+---+
|   |   | Q |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   | Q |   |
+---+---+---+---+---+---+---+---+
|   | Q |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
|   |   |   | Q |   |   |   |   |
+---+---+---+---+---+---+---+---+
Queen positions: (0,0), (1,4), (2,7), (3,5), (4,2), (5,6), (6,1), (7,3)
```

### Logic Puzzles
```bash
$ python -m mcp_server.server run-example logic_puzzles

Solving Simple Logic Puzzle:
Solution:
Position 1: Alice has Cat in Green house
Position 2: Bob has Dog in Red house  
Position 3: Carol has Fish in Blue house

Solving the Famous Zebra Puzzle (Einstein's Riddle)...
ANSWERS:
Who owns the zebra? Ukrainian (House 5)
Who drinks water? Japanese (House 2)
```

## HTTP API Examples

### Classic Problem Solving

#### Australian Map Coloring
```python
import requests

response = requests.post("http://127.0.0.1:8080/solve-map-coloring", json={ 
"regions": ['WA', 'NT', 'SA', 'QLD', 'NSW', 'VIC', 'TAS'], 
"adjacencies": [ 
['WA', 'NT'], ['WA', 'SA'], ['NT', 'SA'], ['NT', 'QLD'], 
['SA', 'QLD'], ['SA', 'NSW'], ['SA', 'VIC'], 
['QLD', 'NSW'], ['NSW', 'VIC'] 
], 
"max_colors": 4
})
```

#### 8-Queens Problem
```python
response = requests.post("http://127.0.0.1:8080/solve-n-queens",
json={"n": 8})
```

## Available Examples

All examples can be run using `gurddy-mcp run-example <name>` or `python -m mcp_server.server run-example <name>`:

### CSP Examples ✅
- **n_queens** - N-Queens problem (4, 6, 8 queens with visual board display)
- **graph_coloring** - Graph coloring (Triangle, Square, Petersen graph, Wheel graph)
- **map_coloring** - Map coloring (Australia, USA Western states, Europe)
- **scheduling** - Scheduling problems (Course scheduling, meeting scheduling, resource allocation)
- **logic_puzzles** - Logic puzzles (Simple logic puzzle, Einstein's Zebra puzzle)
- **optimized_csp** - Advanced CSP techniques (Sudoku solver)

### LP Examples ✅
- **lp** / **optimized_lp** - Linear programming examples:
  - Portfolio optimization with risk constraints
  - Transportation problem (supply chain optimization)
  - Constraint relaxation analysis
  - Performance comparison across problem sizes

### Supported Problem Types

#### CSP Problems
- **N-Queens**: The classic N-Queens problem, supporting chessboards of any size
- **Graph Coloring**: Vertex coloring of arbitrary graph structures  
- **Map Coloring**: Coloring geographic regions, verifying the Four Color Theorem
- **Sudoku**: Solving standard 9×9 Sudoku puzzles
- **Logic Puzzles**: Including classic logical reasoning problems such as the Zebra Puzzle
- **Scheduling**: Course scheduling, meeting scheduling, resource allocation, etc.

#### Optimization Problems
- **Linear Programming**: Linear optimization with continuous variables
- **Integer Programming**: Optimization with discrete variables
- **Production Planning**: Production optimization under resource constraints
- **Mixed Integer Programming**: Optimization with a mix of continuous and discrete variables

## Performance Features

- **Fast Solution**: Typically completes in milliseconds for small to medium-sized problems (N-Queens with N ≤ 12, graph coloring with < 50 vertices)
- **Memory Efficient**: Uses backtracking search and constraint propagation, resulting in a small memory footprint.
- **Extensible**: Supports custom constraints and objective functions
- **Concurrency-Safe**: The HTTP API supports concurrent request processing

## Performance

All examples run efficiently:
- **CSP Examples**: 0.4-0.5 seconds (N-Queens, Graph Coloring, etc.)
- **LP Examples**: 0.8-0.9 seconds (Portfolio optimization, Transportation, etc.)

## Troubleshooting

### Common Errors
- `"gurddy package not available"`: Install with `python -m mcp_server.server install`
- `"No solution found"`: No solution exists under given constraints; try relaxing constraints
- `"Invalid input types"`: Check the data types of input parameters
- `"Unknown example"`: Use `python -m mcp_server.server run-example --help` to see available examples

### Installation Issues
```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individually
pip install gurddy>=0.1.6 pulp>=2.6.0

# Check installation
python -c "import gurddy, pulp; print('All dependencies installed')"
```

### Example Debugging
Run examples directly for debugging:
```bash
# After installing gurddy_mcp
python -c "from mcp_server.examples import n_queens; n_queens.main()"

# Or from source
python mcp_server/examples/n_queens.py
python mcp_server/examples/graph_coloring.py
python mcp_server/examples/logic_puzzles.py
```

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
